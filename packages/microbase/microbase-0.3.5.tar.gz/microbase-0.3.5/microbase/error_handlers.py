from inspect import isclass
from typing import Sequence, Callable, Type, List, Union
from structlog import get_logger

from sanic.http import STATUS_CODES
from sanic.response import BaseHTTPResponse, json
from microbase.exceptions import ApplicationError


log = get_logger('service')


class ErrorHandler(object):
    """

    """

    def __init__(self, exc: Union[Type[BaseException], List[Type[BaseException]]], status_code: int = 500, message=None,
                 callback: Callable[[BaseException], Sequence] = None):
        super().__init__()
        if isinstance(status_code, int) and status_code not in STATUS_CODES:
            raise ApplicationError(f'Unknown status code: {status_code}')

        if isinstance(exc, (list, tuple)):
            self.exceptions = exc
        elif isclass(exc) and issubclass(exc, BaseException):
            self.exceptions = [exc]
        else:
            raise ApplicationError(f'Unknown type of argument {type(exc)}')

        self._code = status_code
        self._message = message

        if callback is not None and not callable(callback):
            raise ApplicationError('Callback must be callable')

        self._callback = callback

    def __call__(self, request, exception: BaseException) -> BaseHTTPResponse:
        log.error(str(exception), exc_info=1)

        status_code = getattr(exception, 'status_code', self._code)
        error_code, message = None, None

        if self._callback is not None:
            error_code, message = self._callback(exception)

        error_code = error_code or status_code
        message = message or self._message or STATUS_CODES.get(status_code) or 'Unknown error'

        return json({'code': error_code, 'message': message}, status=status_code)
