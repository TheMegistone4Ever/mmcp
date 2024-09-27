"""
This module contains the configuration for the models and the criteria.
"""

from enum import Enum


# from ..combinatorial_models import first as cm_first
# from ..linear_models import first, second, third

class Vars:
    beta = .5
    M = 1000
    alpha = .9
    z_min = .8
    weights = .5
    target_difference = .8
    dW = .05
    tolerance = .001


class Criterion(Enum):
    CRITERION_1 = 1
    CRITERION_2 = 2
    CRITERION_3 = 3

    def __int__(self):
        return self.value

    def __str__(self):
        return self.name.replace("_", " ").capitalize()


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
#
#
#
# model_mapping = {
#     "Linear Model 1": first,
#     "Linear Model 2": second,
#     "Linear Model 3": third,
#     "Combinatorial Model": cm_first,
# }
#
# model_mapping = {
#     str(ModelType.LINEAR_MODEL_1): first,
#     str(ModelType.LINEAR_MODEL_2): second,
#     str(ModelType.LINEAR_MODEL_3): third,
#     str(ModelType.COMBINATORIAL_MODEL): cm_first,
# }
#
# criterion_mapping = {
#     "Criterion 1": "criterion_1",
#     "Criterion 2": "criterion_2",
#     "Criterion 3": "criterion_3",
# }
#
# criterion_mapping = {
#     str(Criterion.CRITERION_1): "criterion_1",
#     str(Criterion.CRITERION_2): "criterion_2",
#     str(Criterion.CRITERION_3): "criterion_3",
# }
#
#
