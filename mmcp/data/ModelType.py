from enum import Enum


class ModelType(Enum):
    LINEAR_MODEL_1 = 1
    LINEAR_MODEL_2 = 2
    COMBINATORIAL_MODEL = 3

    def __int__(self):
        return self.value

    def __repr__(self):
        return self.name.replace("_", " ").capitalize()
