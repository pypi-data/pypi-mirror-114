import logging
import os
from dataclasses import dataclass


@dataclass
class CredentialClass:
    _name: str
    _credentials_inited: bool = False

    def __init__(self, **kwargs):
        if self._credentials_inited:
            return
        self._credentials_inited = True

        cls_keys = [
            i
            for i in self.__dict__.keys()
            if not i.startswith("__") and not i.startswith("_")
        ]

        for key in cls_keys:
            env_var = f"{self._name.upper()}_{key.upper()}"
            value = os.getenv(env_var, None)
            if value:
                setattr(self, key, value)
            else:
                logging.debug(
                    f"didn't got {env_var} variable, "
                    f"using standard({getattr(self, key)}) one!"
                )

        for key, value in kwargs.items():
            setattr(self, key, value)


class PostgreSqlCredentials(CredentialClass):
    _name = "postgres"
    host: str = "localhost"
    port: str = "5432"
    password: str = "postgres"
    user: str = "postgres"
    db_name: str = "postgres"

    @property
    def dsn(self):
        return (
            f"postgresql://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.db_name}"
        )

    @property
    def test_db_name(self):
        return f"{self.db_name}_test"
