import numpy as np

np.set_printoptions(precision=2, suppress=True)
np.random.seed(1810)


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

    d = [np.random.rand(num_vars) if np.random.rand() < .5 else None for _ in range(num_elements)]

    return {
        "c": np.random.rand(num_elements, num_vars),
        "A": np.random.rand(num_elements, num_vars, num_vars),  # TODO: MAYBE ERROR
        "b": np.random.rand(num_elements, num_vars),
        "d": d,
        "model_types": np.array([1 if d[i] is None else 2 for i in range(num_elements)]),
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
        "processing_times": np.random.randint(1, num_jobs, num_vars),
        "precedence_graph": {
            j: np.random.choice(np.arange(j), size=np.random.randint(0, min(j, 5)), replace=False)
            for j in range(1, num_vars)
        },
        "weights": np.random.rand(num_vars, num_jobs),
    }
