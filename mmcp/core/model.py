from abc import ABC, abstractmethod


class Model(ABC):
    @abstractmethod
    def solve(self, *args, **kwargs):
        pass
