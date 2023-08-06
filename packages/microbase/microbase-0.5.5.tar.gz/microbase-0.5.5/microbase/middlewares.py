import enum
from collections import defaultdict
from datetime import datetime
from inspect import isawaitable
from structlog import get_logger
from typing import List, Callable, Tuple, Union

from sanic.request import Request

from microbase.exceptions import ApplicationError


log = get_logger('middleware')


class MiddlewareType(enum.Enum):
    request = 'request'
    response = 'response'


class RouteMiddleware:
    def __init__(self, *, request: List[Callable], response: List[Callable]):
        self._before = request
        self._after = response

    def __call__(self, func):
        async def wrapper(request: Request, *args, **kwargs):
            for handler in self._before:
                await self._run_handler(handler, request)

            response = await func(request, *args, **kwargs)

            for handler in self._after:
                await self._run_handler(handler, request, response)
            
            return response

        return wrapper

    @staticmethod
    async def _run_handler(handler, *args, **kwargs):
        res = handler(*args, **kwargs)

        if isawaitable(res):
            await res


def group_middleware_decorators(middlewares: List[Tuple[MiddlewareType, Union[List[str], str], Callable]]):
    def kwargs_factory():
        return {'request': [], 'response': []}

    res = defaultdict(kwargs_factory)
    for m_type, groups, middleware in middlewares:
        if groups is None:
            continue

        if not isinstance(groups, (str, list)):
            raise ApplicationError('Incorrect group type')

        if isinstance(groups, str):
            groups = [groups]

        for group in groups:
            res[group][m_type.value].append(middleware)

    return {k: RouteMiddleware(**v) for k, v in res.items()}

