import logging

logging.basicConfig(filename=r"..\..\logs\mmcp.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

from numpy import set_printoptions, arange, array
from numpy.random import seed, rand, randint, choice

from mmcp.data import LinearModelData, CombinatorialModelData, ModelData
from mmcp.utils import ModelType, Criterion

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
    if model_type == ModelType.LINEAR_MODEL_1:
        return [int(Criterion.CRITERION_1), int(Criterion.CRITERION_2), int(Criterion.CRITERION_3)]
    if model_type == ModelType.LINEAR_MODEL_2:
        return [int(Criterion.CRITERION_1), int(Criterion.CRITERION_2), int(Criterion.CRITERION_3)]
    if model_type == ModelType.LINEAR_MODEL_3:
        return [int(Criterion.CRITERION_1)]
    if model_type == ModelType.COMBINATORIAL_MODEL:
        return [int(Criterion.CRITERION_1), int(Criterion.CRITERION_2)]


def generate_linear_model_data(num_elements=5, num_vars=50) -> LinearModelData:
    """
    Generates synthetic data for the linear models.

    Args:
        num_elements: The number of elements in the system.
        num_vars: The number of variables for each element.

    Returns:
        A LinearModelData object containing the generated data.
    """
    logging.debug(f"Entering generate_linear_model_data with num_elements={num_elements}, num_vars={num_vars}")

    d = [rand(num_vars) if rand() < .5 else None for _ in range(num_elements)]
    model_types = [int(ModelType.LINEAR_MODEL_1) if d[i] is None
                   else choice([int(model) for model in ModelType if model != ModelType.COMBINATORIAL_MODEL])
                   for i in range(num_elements)]
    data = LinearModelData(
        c=rand(num_elements, num_vars),
        A=rand(num_elements, num_vars, num_vars),
        b=rand(num_elements, num_vars),
        d=d,
        criteria=array([choice(_criteria(ModelType(model_type))) for model_type in model_types]),
        model_types=array(model_types),
    )
    logging.info(f"Generated linear model data: {data}")
    return data


def generate_combinatorial_model_data(num_vars=50, num_jobs=50) -> CombinatorialModelData:
    """
    Generates synthetic data for the combinatorial models.

    Args:
        num_vars: The number of variables for each job.
        num_jobs: The number of jobs in the system.

    Returns:
        A CombinatorialModelData object containing the generated data.
    """
    logging.debug(f"Entering generate_combinatorial_model_data with num_vars={num_vars}, num_jobs={num_jobs}")

    data = CombinatorialModelData(
        processing_times=randint(1, num_jobs, num_vars),
        precedence_graph={
            j: choice(arange(j), size=randint(0, min(j, 5)), replace=False)
            for j in range(1, num_vars)
        },
        weights=rand(num_vars, num_jobs),
    )
    logging.info(f"Generated combinatorial model data: {data}")
    return data


def generate_model_data(num_elements=5, num_vars=50, num_jobs=50) -> ModelData:
    """
    Generates synthetic data for the models.

    Args:
        num_elements: The number of elements in the system.
        num_vars: The number of variables for each element.
        num_jobs: The number of jobs in the system.

    Returns:
        A ModelData object containing the generated data.
    """
    logging.debug(
        f"Entering generate_model_data with num_elements={num_elements}, num_vars={num_vars}, num_jobs={num_jobs}")

    linear_data = generate_linear_model_data(num_elements, num_vars)
    linear_data.set_model_type_for_all(
        array([int(ModelType.LINEAR_MODEL_1) if linear_data.d[i] is None
               else choice([int(model) for model in ModelType]) for i in range(num_elements)]))
    linear_data.set_criteria_for_all(array([choice(_criteria(ModelType(model))) for model in linear_data.model_types]))
    data = ModelData(
        *linear_data,
        *generate_combinatorial_model_data(num_vars, num_jobs),
    )
    logging.info(f"Generated model data: {data}")
    return data


if __name__ == "__main__":
    print(generate_model_data())
