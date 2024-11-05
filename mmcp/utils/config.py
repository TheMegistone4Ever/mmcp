from enum import Enum

from .logger_setup import LOGGER

LOGGER.debug(f"Initialized {__name__}")


class Vars:
    LOGGER.debug(f"Initialized {__name__}")
    beta = .5
    M = 1000
    alpha = .9
    z_min = .8
    weights = .5
    target_difference = .8
    dW = .05
    tolerance = .001


class Criterion(Enum):
    LOGGER.debug(f"Initialized {__name__}")
    CRITERION_1 = 1
    CRITERION_2 = 2
    CRITERION_3 = 3

    def __int__(self):
        return self.value

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return self.name.replace("_", " ").capitalize()


class ModelType(Enum):
    LOGGER.debug(f"Initialized {__name__}")
    LINEAR_MODEL_1 = 1
    LINEAR_MODEL_2 = 2
    LINEAR_MODEL_3 = 3
    COMBINATORIAL_MODEL = 4

    def __int__(self):
        return self.value

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return self.name.replace("_", " ").capitalize()
