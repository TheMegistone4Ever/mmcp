from numpy import set_printoptions, array, arange
from numpy.random import seed, rand, randint, choice

set_printoptions(precision=2, suppress=True)
seed(1810)


def generate_linear_model_data(num_elements=5, num_vars=50) -> dict:
    """
    Generates synthetic data for the linear models.

    Args:
        num_elements: The number of elements in the system.
        num_vars: The number of variables for each element.

    Returns:
        A dictionary containing the generated data:
            - c: A list of vectors c for each element.
            - A: A list of matrices A for each element.
            - b: A list of vectors b for each element.
            - d: A list of vectors d for each element (None for linear model 1).
            - model_types: A list of model types (1 for linear model 1, 2 for linear model 2).
    """

    d = [rand(num_vars) if rand() < .5 else None for _ in range(num_elements)]

    return {
        "c": rand(num_elements, num_vars),
        "A": rand(num_elements, num_vars, num_vars),
        "b": rand(num_elements, num_vars),
        "d": d,
        "model_types": array([1 if d[i] is None else 2 for i in range(num_elements)]),
    }


def generate_combinatorial_model_data(num_vars=50, num_jobs=50) -> dict:
    """
    Generates synthetic data for the combinatorial model.

    Args:
        num_vars: The number of variables for the combinatorial model.
        num_jobs: The number of jobs in the combinatorial model.

    Returns:
        A tuple containing:
            - processing_times: A list of processing times for each job.
            - precedence_graph: A dictionary representing the precedence graph.
            - weights: A list of weights for each job.
    """

    return {
        "processing_times": randint(1, num_jobs, num_vars),
        "precedence_graph": {
            j: choice(arange(j), size=randint(0, min(j, 5)), replace=False)
            for j in range(1, num_vars)
        },
        "weights": rand(num_vars, num_jobs),
    }
