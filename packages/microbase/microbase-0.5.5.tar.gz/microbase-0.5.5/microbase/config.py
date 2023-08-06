from sanic_envconfig import EnvConfig
from enum import Enum

__all__ = ['FileStr', 'BaseConfig', 'GeneralConfig']


class LogFormat(Enum):
    json = 'json'
    plain = 'plain'


class FileStr(str):
    pass


class BaseConfig(EnvConfig):
    """
    Базовый класс для создания конфигураций
    """
    pass


@BaseConfig.parse(LogFormat)
def parse_log_format(value: str) -> LogFormat:
    try:
        return LogFormat(value.lower())
    except ValueError:
        return LogFormat.plain


@BaseConfig.parse(FileStr)
def parse_file_str(value: str) -> str:
    from urllib.request import urlopen

    value = value.strip()
    if not value.startswith('file://'):
        return value

    resp = urlopen(value)
    return resp.read().strip().decode('utf-8')


class GeneralConfig(BaseConfig):
    APP_HOST: str = '0.0.0.0'
    APP_PORT: int = 80
    APP_CID: FileStr = '00000000-0000-0000-0000-000000000000'
    APP_TOKEN: FileStr = ''
    APP_PREFIX: str = ''
    APP_DESTINATION: str = ''
    DEBUG: bool = False
    API_HOST: str = 'https://dev.shop-loyalty.ru'
    LOG_FORMAT: LogFormat = LogFormat.plain
    LOG_LEVEL: str = 'INFO'
    WORKERS: int = 0
    SENTRY_DSN: str = ''
