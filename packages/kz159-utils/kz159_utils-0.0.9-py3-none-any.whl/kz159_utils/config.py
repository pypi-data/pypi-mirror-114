import contextlib
from copy import deepcopy
from dataclasses import replace
from logging import getLogger
from os import chdir, getenv
from os.path import abspath, dirname
from typing import Optional

from .data import PostgreSqlCredentials

log = getLogger(__name__)

__all__ = ['config', 'Config']


class Config:
    def __init__(self, abs_path=__file__):
        log.warning('This class is deprecated use pydantic instead')
        self.abs_path = abs_path
        self.try_to_load_dot_env(self.abs_path)
        self.SERVICE_NAME = self.get_service_name(self.abs_path)

        self.postgres_creds: Optional[PostgreSqlCredentials] = None

        self.LOG_LEVEL = getenv("LOG_LEVEL", "INFO")

    @property
    def postgres(self) -> PostgreSqlCredentials:
        if not self.postgres_creds:
            raise AttributeError("Init credential first!")

        return self.postgres_creds

    @postgres.setter
    def postgres(self, value):
        if type(value) != PostgreSqlCredentials:
            raise AttributeError("Init credential first!")
        self.postgres_creds = value

    def init_postgres(self) -> None:
        self.postgres_creds = PostgreSqlCredentials()

    @staticmethod
    def try_to_load_dot_env(abs_path):
        try:
            # noinspection PyUnresolvedReferences
            from dotenv import load_dotenv

            abs_path = abspath(abs_path)
            dir_name = dirname(dirname(abs_path))
            chdir(dir_name)
            return load_dotenv(".env")
        except ImportError:
            pass

    @staticmethod
    def get_service_name(abs_path=__file__):
        abs_path = abspath(abs_path)
        dir_name = dirname(dirname(abs_path))
        return dir_name.split("/")[-1]

    @contextlib.contextmanager
    def temp_variable(self, key, value):
        split_keys = key.split(".")
        if len(split_keys) > 1:
            cached_class = getattr(self, split_keys[0])
            d = {split_keys[1]: value}
            new_dataclass = replace(cached_class, **d)
            setattr(self, split_keys[0], new_dataclass)
            yield self
            self.__setattr__(split_keys[0], cached_class)

        else:
            _class = deepcopy(self)
            cached_variable = getattr(_class, key)
            setattr(self, key, value)
            yield self
            self.__setattr__(key, cached_variable)


config = Config()
