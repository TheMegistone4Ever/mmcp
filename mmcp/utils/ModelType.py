from enum import Enum


class ModelType(Enum):
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
