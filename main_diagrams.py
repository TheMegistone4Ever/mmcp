from matplotlib.lines import Line2D
from matplotlib.pyplot import subplots, savefig, show, legend, tight_layout
from numpy import linspace, mean, isnan

from mmcp.core import Solver
from mmcp.data import generate_model_data
from mmcp.utils import ModelType, Criterion, is_valid_combination, ith_data, measure_execution_time, LOGGER


def generate_performance_diagrams(iterations: int = 10, threads: int = 1, root: str = r".\docs\diagrams\performance"):
    """Generates and saves performance diagrams for different model types and criteria.

    Args:
        iterations: Number of iterations for time measurement.
        threads: Number of threads to use for data generation (not used in current implementation).
        root: Root directory to save the diagrams.
    """
    num_vars_range = linspace(1, 100, 50, dtype=int)

    for model_type in ModelType:
        for criterion in Criterion:
            if not is_valid_combination(model_type, criterion) or criterion == Criterion.CRITERION_3 or \
                    model_type in (ModelType.LINEAR_MODEL_3, ModelType.COMBINATORIAL_MODEL):
                continue

            fig, ax = subplots(1, 1, figsize=(16, 10), dpi=150)
            fig.suptitle(f"Performance: {str(model_type)} - {str(criterion)}")

            times = list()
            if model_type.name.lower().startswith("linear"):
                for num_vars in num_vars_range:
                    LOGGER.info(f"Solving for {str(model_type)} and {str(criterion)} with {num_vars} variables")

                    data = generate_model_data(num_elements=1, num_vars=num_vars, threads=threads)
                    while data.d[0] is None:  # Retry if data generation fails
                        data = generate_model_data(num_elements=1, num_vars=num_vars, threads=threads)
                    data = ith_data(data, 0)
                    solver = Solver(data, model_type, criterion)
                    execution_times = measure_execution_time(solver, iterations=iterations)
                    times.append(execution_times)

                mean_times = mean(times, axis=1)
                last_valid_idx = 0
                for i, time_ms in enumerate(mean_times):
                    if isnan(time_ms):
                        continue

                    if i > last_valid_idx + 1:
                        ax.plot([num_vars_range[last_valid_idx], num_vars_range[i]],
                                [mean_times[last_valid_idx], time_ms], linestyle="--", color="gray", linewidth=5)
                    else:
                        ax.plot([num_vars_range[last_valid_idx], num_vars_range[i]],
                                [mean_times[last_valid_idx], time_ms], color="m", alpha=.5,
                                linewidth=5)
                    last_valid_idx = i

                ax.boxplot(times, positions=num_vars_range, showfliers=False, widths=.5)

                ax.set_xlabel("Number of Variables")
                ax.set_ylabel("Time (seconds)")
                ax.set_title("Linear Model Performance")
                legend(handles=[Line2D([0], [0], color="m", lw=2, label="Mean"),
                                Line2D([0], [0], color="gray", lw=2, linestyle="--", label="Outliers")])
                tight_layout()
                filename = f"{root}\\{model_type.name}_{criterion.name}_[{num_vars_range[0]};{num_vars_range[-1]}].png"
                savefig(filename)
                show()
                LOGGER.info(f"Performance diagram for {model_type} and {criterion} saved to {filename}...")


if __name__ == "__main__":
    generate_performance_diagrams()
