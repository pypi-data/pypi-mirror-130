import logging.config
import sys
from typing import List, Tuple, Callable, Sequence, Type, Union, ClassVar

from sanic import Sanic, Blueprint
from sanic.config import Config
from sanic.exceptions import URLBuildError
from structlog import get_logger

from microbase.config import GeneralConfig, BaseConfig
from microbase.context import _context_mutable, context
from microbase.error_handlers import ErrorHandler
from microbase.exceptions import ApplicationError, log_uncaught
from microbase.logging_config import get_logging_config
from microbase.middlewares import MiddlewareType
from microbase.routes import Route
from microbase.sl_client import get_api_client
from microbase.views import BaseView, HealthCheckView

log = get_logger('microbase')

sys.excepthook = log_uncaught


class Application(object):
    """
    Объект приложения
    """

    def __init__(self):
        # cycling imports resolving
        from microbase.hooks import HookNames, HookHandler

        super(Application, self).__init__()

        self.config = Config(load_env=True)
        self.config.from_object(GeneralConfig)
        self._routes: List[Route] = []
        self._hooks: List[Tuple[HookNames, HookHandler]] = []
        self._before_run: List[Callable] = []
        self._error_handlers: List[ErrorHandler] = []
        self._middlewares: List[Tuple[MiddlewareType, Callable]] = []
        self._init_logging()

        self._sapp: Sanic = None

    def _init_logging(self):
        self._logging_config = get_logging_config(self.config)
        logging.config.dictConfig(self._logging_config)

    def add_config(self, config_obj: ClassVar[BaseConfig]):
        """
        Добавление объекта конфигурации (см. документацию https://github.com/jamesstidard/sanic-envconfig)
        """
        self.config.from_object(config_obj)

    def add_to_context(self, name, obj):
        """
        Добавить объект во внутрь объекта контекста.
        :param name: ключ в контексте
        :param obj: объект
        :return:
        """
        _context_mutable.set(name, obj)

    def add_route(self, route: Route):
        """
        Добавить путь
        :param route:
        :return:
        """
        if not isinstance(route.handler, BaseView):
            raise ApplicationError('Handler must be instance of BaseView class')

        self._routes.append(route)

    def add_routes(self, routes: List[Route]):
        """
        Добавить список путей
        :param routes:
        :return:
        """
        for r in routes:
            self.add_route(r)

    def add_server_hook(self, hook_name, handler):
        """
        Добавить хук
        :param hook_name:
        :param handler:
        :return:
        """
        # cycling imports resolving
        from microbase.hooks import HookNames, HookHandler

        if not isinstance(hook_name, HookNames):
            raise ApplicationError('Hook must be one of HookNames enum')
        hook_handler = HookHandler(self, handler)

        self._hooks.append((hook_name, hook_handler))

    def before_run(self, handler: Callable):
        """
        Обработчик, который запускается перед запуском приложения (метод run)
        :param handler:
        :return:
        """
        self._before_run.append(handler)

    def add_error_handler(self, exc: Union[Type[BaseException], List[Type[BaseException]]], status_code: int = 500,
                          message=None, callback: Callable[[BaseException], Sequence] = None):
        """
        Добавить обработчик ошибок
        :param exc:
        :param status_code:
        :param message:
        :param callback:
        :return:
        """
        handler = ErrorHandler(exc, status_code, message, callback)
        self._error_handlers.append(handler)

    def add_middleware(self, middleware_type: MiddlewareType, middleware: Callable):
        """
        Добавить middleware
        :param middleware_type:
        :param middleware:
        :return:
        """
        if not isinstance(middleware_type, MiddlewareType):
            raise ApplicationError('middleware_type must be Middleware enum')

        if not callable(middleware):
            raise ApplicationError('middleware must be callable')

        self._middlewares.append((middleware_type, middleware))

    def get_url(self, name_or_view: Union[str, BaseView], **kwargs):
        from urllib.parse import urlsplit

        if isinstance(name_or_view, type) and issubclass(name_or_view, BaseView):
            name_or_view = name_or_view.__name__

        name = f'{self.config.APP_PREFIX}.{name_or_view}'
        api_host = urlsplit(self.config.API_HOST)

        if self._sapp is None:
            raise ApplicationError('Could not get url before run')

        try:
            return self._sapp.url_for(name, _external=True, _server=api_host.netloc, _scheme=api_host.scheme, **kwargs)
        except URLBuildError as e:
            raise ApplicationError(f'Endpoint with name `{name_or_view}` was not found', e)

    def _apply_routes(self, sapp: Sanic):
        b = Blueprint(self.config.APP_PREFIX, url_prefix=self.config.APP_PREFIX)

        for r in self._routes:
            b.add_route(r.handler, r.uri, methods=r.methods, strict_slashes=r.strict_slashes, name=r.name)

        sapp.blueprint(b)

    def _apply_hooks(self, sapp: Sanic):
        for hook_name, hook_handler in self._hooks:
            sapp.listener(hook_name.value)(hook_handler)

    def _apply_error_handlers(self, sapp: Sanic):
        for handler in self._error_handlers:
            sapp.exception(*handler.exceptions)(handler)

        default_handler = ErrorHandler(Exception)
        sapp.exception(Exception)(default_handler)

    def _apply_middlewares(self, sapp: Sanic):
        for m_type, middleware in self._middlewares:
            sapp.middleware(m_type.value)(middleware)

    def _num_workers(self):
        if self.config.WORKERS > 0:
            return self.config.WORKERS
        from multiprocessing import cpu_count
        return cpu_count() * 2 + 1

    def _sanic_prepare(self):
        self._sapp = Sanic(__name__, log_config=self._logging_config)
        self._sapp.config = self.config

        self._sapp.add_route(HealthCheckView(context), '/health')
        self._apply_routes(self._sapp)
        self._apply_hooks(self._sapp)
        self._apply_error_handlers(self._sapp)
        self._apply_middlewares(self._sapp)

    def run(self):
        """
        Запуск приложения
        :return:
        """
        self._sanic_prepare()

        num_workers = self._num_workers()

        for handler in self._before_run:
            handler(self, context)

        self._sapp.run(host=self.config.APP_HOST, port=self.config.APP_PORT, debug=self.config.DEBUG,
                       workers=num_workers)


def build_sl_app():
    """
    Создание приложения заточенного под SL:

    * sl_client в объекте контекста

    :return:
    """
    from microbase.hooks import HookNames
    from .context import Context

    async def client_to_context(app: Application, *_):
        sl_client = get_api_client(app.config)
        app.add_to_context('sl_client', sl_client)

    async def close_client(app: Application, ctx: Context, *_):
        from sl_api_client import ApiClient
        sl_client: ApiClient = ctx.sl_client
        close = getattr(sl_client.rest_client.pool_manager, 'close', None)
        if close is not None:
            await close()

    sl_app = Application()
    sl_app.add_server_hook(HookNames.before_server_start, client_to_context)
    sl_app.add_server_hook(HookNames.after_server_stop, close_client)

    return sl_app


if __name__ == '__main__':
    a = build_sl_app()
    a.run()
