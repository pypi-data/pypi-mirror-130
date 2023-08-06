from typing import Iterable

from microbase.exceptions import RouteError
from microbase.views import BaseView


class Route(object):
    def __init__(self, handler: BaseView, uri: str, methods: Iterable = frozenset({'GET'}),
                 strict_slashes: bool = False, name: str = None):
        super(Route, self).__init__()

        if not isinstance(handler, BaseView):
            raise RouteError('Handler must be instance of BaseView class')

        self._handler = handler
        self._uri = uri
        self._methods = methods
        self._strict_slashes = strict_slashes

        self._name = name
        if self._name is None:
            self._name = self._handler.__name__

    @property
    def handler(self) -> BaseView:
        return self._handler

    @property
    def uri(self) -> str:
        return self._uri

    @property
    def methods(self) -> Iterable:
        return self._methods

    @property
    def strict_slashes(self) -> bool:
        return self._strict_slashes

    @property
    def name(self):
        return self._name
