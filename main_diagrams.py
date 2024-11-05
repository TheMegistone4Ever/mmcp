import logging

from os import makedirs
from os.path import join

# Configure logging
LOGS_DIR = "./logs"
makedirs(LOGS_DIR, exist_ok=True)
logging.basicConfig(filename=join(LOGS_DIR, "mmcp.log"), level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")
LOGGER = logging.getLogger(__name__)
LOGGER.debug(f"Initialized {__name__}")

from time import time
from typing import NamedTuple, List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

from mmcp.core import SolverError, Solver
from mmcp.data import ModelData, generate_model_data
from mmcp.utils import ModelType, Criterion


# TODO: Move to Utils
def _measure_execution_time(solver: Solver, warmup: int = 10, iterations: int = 10) -> List[float]:
    """Measures the execution time of the solver.

    Args:
        solver: The Solver instance.
        warmup: Number of warmup iterations.
        iterations: Number of measurement iterations.

    Returns:
        A list of execution times in seconds. NaN is appended for SolverErrors.
    """
    times = list()
    for _ in range(warmup + iterations):
        try:
            start_time = time()
            solver.solve()
            end_time = time()
            times.append(end_time - start_time)
        except SolverError as e:
            LOGGER.error(f"Solver error: {e}")
            times.append(np.nan)
    return times[warmup:]


# TODO: Move to Utils
# noinspection PyProtectedMember
def _get_model_data_element(data: NamedTuple, element_idx: int) -> ModelData:
    """Retrieves data for a specific element index from a NamedTuple.

    Args:
        data: The NamedTuple containing model data.
        element_idx: The index of the element to retrieve.

    Returns:
        A ModelData instance for the specified element.
    """
    LOGGER.debug(f"Retrieving data for element {element_idx + 1}.")
    return ModelData(**{k: list(v)[element_idx] for k, v in data._asdict().items() if len(v) > element_idx})


# TODO: Move to Utils
def _is_valid_combination(model_type: ModelType, criterion: Criterion) -> bool:
    """Checks if the model type and criterion combination is valid."""
    if model_type == ModelType.LINEAR_MODEL_3 and criterion != Criterion.CRITERION_1:
        return False
    if model_type == ModelType.COMBINATORIAL_MODEL and criterion == Criterion.CRITERION_3:
        return False
    return True


def generate_performance_diagrams(iterations: int = 10, threads: int = 1):
    """Generates and saves performance diagrams for different model types and criteria.

    Args:
        iterations: Number of iterations for time measurement.
        threads: Number of threads to use for data generation (not used in current implementation).

    """
    num_vars_range = np.linspace(1, 100, 50, dtype=int)

    for model_type in ModelType:
        for criterion in Criterion:
            if not _is_valid_combination(model_type, criterion) or criterion == Criterion.CRITERION_3 or \
                    model_type in (ModelType.LINEAR_MODEL_3, ModelType.COMBINATORIAL_MODEL):
                continue

            fig, ax = plt.subplots(1, 1, figsize=(16, 8), dpi=150)
            fig.suptitle(f"Performance: {model_type.name} - {criterion.name}")

            times = list()
            if model_type.name.lower().startswith("linear"):
                for num_vars in num_vars_range:
                    LOGGER.info(f"Solving for {model_type} and {criterion} with {num_vars} variables")

                    data = generate_model_data(num_elements=1, num_vars=num_vars, threads=threads)
                    while data.d[0] is None:  # Retry if data generation fails
                        data = generate_model_data(num_elements=1, num_vars=num_vars, threads=threads)
                    data = _get_model_data_element(data, 0)
                    solver = Solver(data, model_type, criterion)
                    execution_times = _measure_execution_time(solver, iterations=iterations)
                    times.append(execution_times)

                mean_times = np.nanmean(times, axis=1)
                last_valid_idx = 0
                for i, time_ms in enumerate(mean_times):
                    if np.isnan(time_ms):
                        continue

                    if i > last_valid_idx + 1:
                        ax.plot([num_vars_range[last_valid_idx], num_vars_range[i]],
                                [mean_times[last_valid_idx], time_ms], linestyle='dashed', color='gray', linewidth=5)
                    else:
                        ax.plot([num_vars_range[last_valid_idx], num_vars_range[i]],
                                [mean_times[last_valid_idx], time_ms], linestyle='solid', color='magenta', alpha=0.5,
                                linewidth=5)
                    last_valid_idx = i

                ax.boxplot(times, positions=num_vars_range, showfliers=False, widths=0.5)

                ax.set_xlabel("Number of Variables")
                ax.set_ylabel("Time (seconds)")
                ax.set_title("Linear Model Performance")
                plt.legend(handles=[Line2D([0], [0], color='magenta', lw=2, label='Mean'),
                                    Line2D([0], [0], color='gray', lw=2, linestyle='dashed', label='Outliers')])
                plt.tight_layout()
                plt.savefig(f"performance_{model_type.name}_{criterion.name}.png")
                plt.show()


if __name__ == "__main__":
    generate_performance_diagrams()
