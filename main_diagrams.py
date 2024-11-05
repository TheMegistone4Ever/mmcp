import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

from mmcp.core import Solver
from mmcp.data import generate_model_data
from mmcp.utils import ModelType, Criterion, is_valid_combination, ith_data, measure_execution_time, LOGGER


def generate_performance_diagrams(iterations: int = 10, threads: int = 1):
    """Generates and saves performance diagrams for different model types and criteria.

    Args:
        iterations: Number of iterations for time measurement.
        threads: Number of threads to use for data generation (not used in current implementation).

    """
    num_vars_range = np.linspace(1, 500, 100, dtype=int)

    for model_type in ModelType:
        for criterion in Criterion:
            if not is_valid_combination(model_type, criterion) or criterion == Criterion.CRITERION_3 or \
                    model_type in (ModelType.LINEAR_MODEL_3, ModelType.COMBINATORIAL_MODEL):
                continue

            fig, ax = plt.subplots(1, 1, figsize=(16, 10), dpi=150)
            fig.suptitle(f"Performance: {model_type.name} - {criterion.name}")

            times = list()
            if model_type.name.lower().startswith("linear"):
                for num_vars in num_vars_range:
                    LOGGER.info(f"Solving for {model_type} and {criterion} with {num_vars} variables")

                    data = generate_model_data(num_elements=1, num_vars=num_vars, threads=threads)
                    while data.d[0] is None:  # Retry if data generation fails
                        data = generate_model_data(num_elements=1, num_vars=num_vars, threads=threads)
                    data = ith_data(data, 0)
                    solver = Solver(data, model_type, criterion)
                    execution_times = measure_execution_time(solver, iterations=iterations)
                    times.append(execution_times)

                mean_times = np.mean(times, axis=1)
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

                LOGGER.info(f"Performance diagram for {model_type} and {criterion} saved to "
                            f"performance_{model_type.name}_{criterion.name}.png")


if __name__ == "__main__":
    generate_performance_diagrams()
