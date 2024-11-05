from abc import ABC, abstractmethod

from ..utils.logger_setup import LOGGER


class Model(ABC):
    LOGGER.debug(f"Initialized {__name__}")

    @abstractmethod
    def solve(self, *args, **kwargs):
        pass
