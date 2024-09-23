import numpy as np

np.set_printoptions(precision=2, suppress=True)
np.random.seed(1810)


def generate_linear_model_data(num_elements=5, num_vars=50):
    """
    Generates synthetic data for the linear models.

    Args:
        num_elements: The number of elements in the system.
        num_vars: The number of variables for each element.

    Returns:
        A tuple containing lists of data for each element:
            - c_list: List of coefficient vectors.
            - A_list: List of constraint matrices.
            - b_list: List of constraint bound vectors.
            - d_list: List of private resource vectors (can be None for elements using the first linear model).
            - model_types: List indicating the type of model for each element (1 or 2).
    """

    c_list = [np.random.rand(num_vars) for _ in range(num_elements)]
    A_list = [np.random.rand(num_vars, num_vars) for _ in range(num_elements)]
    b_list = [np.random.rand(num_vars) for _ in range(num_elements)]
    d_list = [np.random.rand(num_vars) if np.random.rand() < .5 else None for _ in range(num_elements)]
    model_types = [1 if d_list[i] is None else 2 for i in range(num_elements)]

    return c_list, A_list, b_list, d_list, model_types


def generate_combinatorial_model_data(num_jobs=50):
    """
    Generates synthetic data for the combinatorial model.

    Args:
        num_jobs: The number of jobs.

    Returns:
        A tuple containing:
            - processing_times: A list of processing times for each job.
            - precedence_graph: A dictionary representing the precedence graph.
            - weights: A list of weights for each job.
    """

    processing_times = np.random.randint(1, 10, size=num_jobs)
    precedence_graph = {}
    for j in range(1, num_jobs):
        num_predecessors = np.random.randint(0, min(j, 5))  # Up to 5 predecessors
        predecessors = np.random.choice(np.arange(j), size=num_predecessors, replace=False)
        precedence_graph[j] = list(predecessors)
    weights = np.random.rand(num_jobs)

    return processing_times, precedence_graph, weights
