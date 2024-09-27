from abc import ABC, abstractmethod

from .model import Model


class Criterion(ABC):
    @abstractmethod
    def apply(self, model: Model, *data, **kwargs):
        pass
