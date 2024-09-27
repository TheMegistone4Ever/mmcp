"""
This module contains the configuration for the MMCP package.
"""
from ..combinatorial_models import first as cm_first
from ..linear_models import first, second, third


class Vars:
    beta = .5
    M = 1000
    alpha = .9
    z_min = .8
    weights = .5
    target_difference = .8
    dW = .05
    tolerance = .001


model_mapping = {
    "Linear Model 1": first,
    "Linear Model 2": second,
    "Linear Model 3": third,
    "Combinatorial Model": cm_first,
}

criterion_mapping = {
    "Criterion 1": "criterion_1",
    "Criterion 2": "criterion_2",
    "Criterion 3": "criterion_3",
}
