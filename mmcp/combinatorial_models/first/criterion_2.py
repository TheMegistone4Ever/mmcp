from ortools.linear_solver import pywraplp


def solve(processing_times, precedence_graph, initial_weights, target_differences):
    """
    Solves the second criterion for the combinatorial model (approximation using LP relaxation and iterative adjustment).

    Args:
        processing_times: A list of processing times for each job.
        precedence_graph: A dictionary representing the precedence graph (key: job, value: list of predecessors).
        initial_weights: A list of initial weights for each job.
        target_differences: A list of target differences in completion times between pairs of jobs.

    Returns:
        A list of job completion times (approximation).
    """
    num_jobs = len(processing_times)
    weights = initial_weights.copy()
    M = 1000  # Large constant
    tolerance = 1e-6  # Tolerance for convergence

    for _ in range(100):  # Limit iterations
        completion_times = solve_weighted_completion_time(processing_times, precedence_graph, weights, M)

        max_diff = 0
        for i, j, target_diff in target_differences:
            diff = abs(completion_times[i] - completion_times[j] - target_diff)
            if diff > max_diff:
                max_diff = diff

        if max_diff < tolerance:
            break

        # Adjust weights based on differences (example logic)
        for i, j, target_diff in target_differences:
            if completion_times[i] - completion_times[j] > target_diff:
                weights[i] -= 0.1  # Decrease weight for job i
                weights[j] += 0.1  # Increase weight for job j
            else:
                weights[i] += 0.1
                weights[j] -= 0.1

    return completion_times


def solve_weighted_completion_time(processing_times, precedence_graph, weights, M):
    """
    Helper function: Solves the weighted completion time problem using LP relaxation (similar to Criterion 1).
    """
    num_jobs = len(processing_times)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    completion_times = [solver.NumVar(0, solver.infinity(), f'C_{j}') for j in range(num_jobs)]

    # Precedence constraints
    for j in range(num_jobs):
        for pred in precedence_graph.get(j, []):
            solver.Add(completion_times[j] >= completion_times[pred] + processing_times[j])

    # Non-overlap constraints (simplified for LP relaxation)
    for j in range(num_jobs):
        for k in range(j + 1, num_jobs):
            solver.Add(completion_times[j] >= completion_times[k] + processing_times[j] - M * (
                    1 - solver.IntVar(0, 1, f'y_{j}_{k}')))
            solver.Add(completion_times[k] >= completion_times[j] + processing_times[k] - M * solver.IntVar(0, 1,
                                                                                                            f'y_{j}_{k}'))

    # Objective: Minimize weighted completion times
    objective = solver.Objective()
    for j in range(num_jobs):
        objective.SetCoefficient(completion_times[j], weights[j])
    objective.SetMinimization()

    solver.Solve()
    return [c.solution_value() for c in completion_times]
