from dataclasses import dataclass, field
from os import path, environ

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


@dataclass
class Config:
    BASE_DIR = base_dir
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True
    DB_URL: str = None


@dataclass
class LocalConfig(Config):
    PROJ_RELOAD: bool = True
    DB_URL: str = field(default='mysql+pymysql://root:adsf25did@localhost:13306/fastapi')


@dataclass
class ProdConfig(Config):
    PROJ_RELOAD: bool = False


def conf():
    config = dict(prod=ProdConfig(), local=LocalConfig())
    return config.get(environ.get('API_ENV', 'local'))
