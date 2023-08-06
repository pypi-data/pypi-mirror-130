from contextlib import redirect_stdout

from sanic.config import Config
from sl_api_client import Configuration, ApiClient


class OutputWrapper(object):
    class Writable:
        def __init__(self, logger):
            self.logger = logger
            self._buffer = []

        def write(self, string):
            if string == '\n':
                self.logger.debug(''.join(self._buffer))
                self._buffer = []
            else:
                self._buffer.append(string)

        def flush_buffer(self):
            if len(self._buffer):
                self.logger.debug(''.join(self._buffer))

    def __init__(self, wrapped_object, logger):
        super(OutputWrapper, self).__init__()
        self._stdout = self.Writable(logger)
        self._wrapped_obj = wrapped_object

    def __getattr__(self, item):
        def func(*args, **kwargs):
            with redirect_stdout(self._stdout):
                res = real_attr(*args, **kwargs)
                self._stdout.flush_buffer()
                return res

        real_attr = getattr(self._wrapped_obj, item)
        if not callable(real_attr):
            return real_attr

        return func


def get_api_client(config: Config, cid: str = None):
    cfg = Configuration()
    cfg.host = config.API_HOST
    cfg.debug = config.DEBUG
    cfg.api_key['x-cid'] = cid or config.APP_CID
    cfg.api_key['x-token'] = config.APP_TOKEN
    client = ApiClient(configuration=cfg)

    # loggers handlers reset
    for logger in cfg.logger.values():
        for h in logger.handlers.copy():
            logger.removeHandler(h)

    client = OutputWrapper(client, cfg.logger['package_logger'])

    return client
