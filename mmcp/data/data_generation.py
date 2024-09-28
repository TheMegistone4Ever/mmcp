import logging

logging.basicConfig(filename=r"..\..\logs\mmcp.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

from numpy import set_printoptions, arange
from numpy.random import seed, rand, randint, choice

from mmcp.data import LinearModelData, CombinatorialModelData, ModelData
from mmcp.utils import ModelType

set_printoptions(precision=2, suppress=True)
seed(1810)


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

    data = LinearModelData(
        c=rand(num_elements, num_vars),
        A=rand(num_elements, num_vars, num_vars),
        b=rand(num_elements, num_vars),
        d=d,
        model_types=randint(int(ModelType.LINEAR_MODEL_1), int(ModelType.COMBINATORIAL_MODEL) + 1, num_elements),
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

    data = ModelData(
        *generate_linear_model_data(num_elements, num_vars),
        *generate_combinatorial_model_data(num_vars, num_jobs),
    )
    logging.info(f"Generated model data: {data}")
    return data


if __name__ == "__main__":
    print(generate_model_data())
