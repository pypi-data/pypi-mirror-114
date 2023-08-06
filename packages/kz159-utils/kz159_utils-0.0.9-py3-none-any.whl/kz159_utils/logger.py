import sys
from logging import Formatter, StreamHandler, getLogger

from kz159_utils import config

__all__ = ['CustomLogger']


class CustomLogger:
    """
    Custom logger, better to init
    this in __init__.py of project
    """

    def __init__(self, root):
        self._root = root
        self._logger = None

        self.setup_logger()

    def setup_logger(self):
        self._logger = getLogger(config.SERVICE_NAME)
        self._logger.setLevel(config.LOG_LEVEL)
        h1 = StreamHandler(sys.stdout)
        h1.setFormatter(Formatter('%(name)s[%(levelname).1s] - %(message)s'))
        self._logger.addHandler(h1)

    @property
    def logger(self):
        return self._logger

    def ll(self):
        pass
