from concurrent.futures import ThreadPoolExecutor, as_completed

from numpy import set_printoptions, arange, array
from numpy.random import seed, rand, randint, choice

from mmcp.data import LinearModelData, CombinatorialModelData, ModelData
from mmcp.utils import ModelType, Criterion
from ..utils.logger_setup import LOGGER

set_printoptions(precision=2, suppress=True)
seed(1810)


def _criteria(model_type: ModelType) -> list[int]:
    """
    Returns the criteria for the given model type.

    Args:
        model_type: The model type.

    Returns:
        A list of criteria.
    """
    LOGGER.debug(f"Entering _criteria with model_type={model_type}")

    if model_type == ModelType.LINEAR_MODEL_1:
        return [int(Criterion.CRITERION_1), int(Criterion.CRITERION_2), int(Criterion.CRITERION_3)]
    if model_type == ModelType.LINEAR_MODEL_2:
        return [int(Criterion.CRITERION_1), int(Criterion.CRITERION_2), int(Criterion.CRITERION_3)]
    if model_type == ModelType.LINEAR_MODEL_3:
        return [int(Criterion.CRITERION_1)]
    if model_type == ModelType.COMBINATORIAL_MODEL:
        return [int(Criterion.CRITERION_1), int(Criterion.CRITERION_2)]


def generate_linear_model_data(num_elements=5, num_vars=50, threads=1) -> LinearModelData:
    """
    Generates synthetic data for the linear models.

    Args:
        num_elements: The number of elements in the system.
        num_vars: The number of variables for each element.
        threads: The number of threads to use for data generation.

    Returns:
        A LinearModelData object containing the generated data.
    """
    LOGGER.debug(f"Entering generate_linear_model_data with num_elements={num_elements}, num_vars={num_vars}, "
                 f"threads={threads}")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(lambda: [rand(num_vars) if rand() < .5 else None for _ in range(num_elements)]): "d",
            executor.submit(lambda: rand(num_elements, num_vars)): "c",
            executor.submit(lambda: rand(num_elements, num_vars, num_vars)): "A",
            executor.submit(lambda: rand(num_elements, num_vars)): "b",
        }

        results = dict()
        for future in as_completed(futures):
            data_type = futures[future]
            results[data_type] = future.result()

    d = results["d"]
    model_types = [int(ModelType.LINEAR_MODEL_1) if d[i] is None
                   else choice([int(model) for model in ModelType if model != ModelType.COMBINATORIAL_MODEL])
                   for i in range(num_elements)]
    data = LinearModelData(
        c=results["c"],
        A=results["A"],
        b=results["b"],
        d=d,
        criteria=array([choice(_criteria(ModelType(model_type))) for model_type in model_types]),
        model_types=array(model_types),
    )
    LOGGER.info(f"Generated linear model data: {data}")
    return data


def generate_combinatorial_model_data(num_vars=50, num_jobs=50, threads=1) -> CombinatorialModelData:
    """
    Generates synthetic data for the combinatorial models.

    Args:
        num_vars: The number of variables for each job.
        num_jobs: The number of jobs in the system.
        threads: The number of threads to use for data generation.

    Returns:
        A CombinatorialModelData object containing the generated data.
    """
    LOGGER.debug(f"Entering generate_combinatorial_model_data with num_vars={num_vars}, num_jobs={num_jobs}, "
                 f"threads={threads}")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(lambda: randint(1, num_jobs, num_vars)): "processing_times",
            executor.submit(lambda: ((j, choice(arange(j), size=randint(0, min(j, 5)), replace=False))
                                     for j in range(1, num_vars))
                            ): "precedence_graph",
            executor.submit(lambda: rand(num_vars, num_jobs)): "weights",
        }
        results = {}
        for future in as_completed(futures):
            data_type = futures[future]
            results[data_type] = future.result()

    precedence_graph_dict = {}
    for node, predecessors in results["precedence_graph"]:
        precedence_graph_dict[node] = predecessors
    data = CombinatorialModelData(
        processing_times=results["processing_times"],
        precedence_graph=precedence_graph_dict,
        weights=results["weights"],
    )
    LOGGER.info(f"Generated combinatorial model data: {data}")
    return data


def generate_model_data(num_elements=5, num_vars=50, num_jobs=50, threads=1) -> ModelData:
    """
    Generates synthetic data for the models.

    Args:
        num_elements: The number of elements in the system.
        num_vars: The number of variables for each element.
        num_jobs: The number of jobs in the system.
        threads: The number of threads to use for data generation.

    Returns:
        A ModelData object containing the generated data.
    """
    LOGGER.debug(f"Entering generate_model_data with num_elements={num_elements}, num_vars={num_vars}, "
                 f"num_jobs={num_jobs}, threads={threads}")

    linear_data = generate_linear_model_data(num_elements, num_vars, threads)
    linear_data.set_model_type_for_all(
        array([int(ModelType.LINEAR_MODEL_1) if linear_data.d[i] is None
               else choice([int(model) for model in ModelType]) for i in range(num_elements)]))
    linear_data.set_criteria_for_all(array([choice(_criteria(ModelType(model))) for model in linear_data.model_types]))
    data = ModelData(
        *linear_data,
        *generate_combinatorial_model_data(num_vars, num_jobs, threads),
    )
    LOGGER.info(f"Generated model data: {data}")
    return data


if __name__ == "__main__":
    print(generate_model_data(threads=4))
