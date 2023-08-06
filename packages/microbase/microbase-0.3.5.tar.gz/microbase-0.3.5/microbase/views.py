import abc
import asyncio
import functools
import inspect
import textwrap
from logging import Logger
from traceback import format_exception
from typing import Callable

from marshmallow import MarshalResult
from sanic.request import Request
from sanic.response import BaseHTTPResponse, text, json
from sl_api_client import ErrorModel
from structlog import get_logger

from microbase.data import BaseSchema, InputSchema
from .context import Context

try:
    from rapidjson import dumps as json_dumps
except ImportError:
    from json import dumps as json_dumps


log: Logger = get_logger('microbase')


class BaseView(metaclass=abc.ABCMeta):
    """
    Базовый класс для реализации view
    """
    _event_callbacks = {}

    def __init__(self, context: Context):
        super(BaseView, self).__init__()
        self.context = context
        self.__name__ = self.__class__.__name__

    async def __call__(self, request: Request, *args, **kwargs):
        try:
            response = await self.handle(request, *args, **kwargs)
        except BaseException as e:
            await self.trigger_events('view.on_exception', request, e)
            raise
        else:
            await self.trigger_events('view.on_complete', request, response)

        return response

    @abc.abstractmethod
    async def handle(self, request: Request, *args, **kwargs) -> BaseHTTPResponse:
        raise NotImplementedError

    @classmethod
    def event(cls, event_name):
        """
        Декоратор, который добавляет обработчик для события `event_name`

        :param event_name:
        :return:
        """
        def wrapped(callback: Callable):
            if not inspect.iscoroutinefunction(callback):
                raise TypeError('Callback must be coroutine function')

            cls._event_callbacks.setdefault(cls, {}).setdefault(event_name, set()).add(callback)
            return callback

        return wrapped

    async def trigger_events(self, event_name, *args, **kwargs) -> bool:
        """
        Запуск обработки событий с имененем указазным в `event_name`

        :param event_name:
        :param args:
        :param kwargs:
        :return:
        """
        callbacks = set()
        for cls, events in self._event_callbacks.items():
            if not isinstance(self, cls):
                continue

            callbacks |= events.get(event_name, set())
        res = await asyncio.gather(*map(lambda _: _(self, *args, **kwargs), callbacks), return_exceptions=True)

        exceptions = list(filter(lambda _: isinstance(_, BaseException), res))
        if len(exceptions) > 0:
            log.error(f'While processing event, named `{event_name}` callbacks, errors occured', event_name=event_name,
                      exceptions=[''.join(format_exception(None, e, e.__traceback__)) for e in exceptions])
            return False

        return True


class HealthCheckView(BaseView):
    async def handle(self, request: Request, *args, **kwargs) -> BaseHTTPResponse:
        return text('OK')


class BaseSchemaView(BaseView, metaclass=abc.ABCMeta):
    @property
    def schema(self) -> BaseSchema:
        raise NotImplementedError

    @property
    def status_code(self) -> int:
        return 200

    async def handle(self, request: Request, *args, **kwargs) -> BaseHTTPResponse:
        result = await self._handle(request, *args, **kwargs)

        dump_result: MarshalResult = self.schema.dump(result)

        if len(dump_result.errors):
            raise ErrorModel(code=500, message='Ошибка во время вывода результата')

        return json(dump_result.data, dumps=json_dumps, status=self.status_code)

    async def _handle(self, request: Request, *args, **kwargs):
        raise NotImplementedError


class _InputModelsDecorator(object):
    def __init__(self, *, body_schema: InputSchema = None, query_schema: InputSchema = None):
        self.body_schema = body_schema
        self.query_schema = query_schema

    def __call__(self, method):
        @functools.wraps(method)
        def wrapper(view: BaseSchemaView, request: Request, *args, **kwargs):
            if self.query_schema is not None:
                parse_result: MarshalResult = self.query_schema.load(request.raw_args)

                if len(parse_result.errors):
                    raise ErrorModel(code=400,
                                     message=textwrap.shorten(str(parse_result.errors), 500, placeholder='...'))

                kwargs['query'] = parse_result.data

            if self.body_schema is not None and request.method in {'PUT', 'POST'}:
                parse_result: MarshalResult = self.body_schema.load(request.json)

                if len(parse_result.errors):
                    raise ErrorModel(code=400,
                                     message=textwrap.shorten(str(parse_result.errors), 500, placeholder='...'))

                kwargs['body'] = parse_result.data

            return method(view, request, *args, **kwargs)

        return wrapper


input_models = _InputModelsDecorator
