from time import time
from typing import List, NamedTuple

from numpy import nan

from .config import ModelType, Criterion
from .logger_setup import LOGGER
from ..core.exception import SolverError
from ..core.solver import Solver
from ..data import ModelData

LOGGER.debug(f"Initialized {__name__}")


# noinspection PyProtectedMember
def ith_data(data: NamedTuple, element_idx: int):
    """
    Get the data for the given element index.

    Args:
        element_idx: The index of the element.
        data: The NamedTuple containing the data.

    Returns:
        The data for the element.
    """
    LOGGER.debug(f"Retrieving data for element {element_idx + 1}.")

    return ModelData(**{k: list(v)[element_idx] for k, v in data._asdict().items() if len(v) > element_idx})


def measure_execution_time(solver: Solver, warmup: int = 10, iterations: int = 10) -> List[float]:
    """Measures the execution time of the solver.

    Args:
        solver: The Solver instance.
        warmup: Number of warmup iterations.
        iterations: Number of measurement iterations.

    Returns:
        A list of execution times in seconds. NaN is appended for SolverErrors.
    """
    LOGGER.debug(f"Measuring execution time for {solver}, {warmup} warmup iterations, {iterations} iterations.")
    print(f"Measuring execution time for {solver}, {warmup} warmup iterations, {iterations} iterations.")

    times = list()
    for _ in range(warmup + iterations):
        try:
            start_time = time()
            solver.solve()
            end_time = time()
            times.append(end_time - start_time)
        except SolverError as e:
            LOGGER.error(f"Solver error: {e}")
            times.append(nan)
    return times[warmup:]


def is_valid_combination(model_type: ModelType, criterion: Criterion) -> bool:
    """Checks if the model type and criterion combination is valid."""
    LOGGER.debug(f"Checking if {model_type} and {criterion} is a valid combination.")

    if model_type == ModelType.LINEAR_MODEL_3 and criterion != Criterion.CRITERION_1:
        return False
    if model_type == ModelType.COMBINATORIAL_MODEL and criterion == Criterion.CRITERION_3:
        return False
    return True
