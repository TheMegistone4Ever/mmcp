from ortools.linear_solver import pywraplp

from mmcp.core import SolverError


def solve(processing_times, precedence_graph, weights, M):
    """
    Solves the first criterion for the combinatorial model (approximation using LP relaxation).

    Args:
        processing_times: A list of processing times for each job.
        precedence_graph: A dictionary representing the precedence graph (key: job, value: list of predecessors).
        weights: A list of weights for each job.
        M: A large constant.

    Returns:
        A list of job completion times (approximation).
    """

    num_jobs = len(processing_times) if isinstance(processing_times, list) else 1
    solver = pywraplp.Solver.CreateSolver("GLOP")

    # Variables: completion times (continuous relaxation)
    completion_times = [solver.NumVar(0, solver.infinity(), f"C_{j}") for j in range(num_jobs)]

    # Constraints:
    # 1. Precedence constraints
    for j in range(num_jobs):
        for pred in precedence_graph.get(j, list()):
            solver.Add(completion_times[j] >= completion_times[pred] + processing_times[j])

    # 2. Non-overlap constraints (simplified for LP relaxation)
    #    Note: This is an approximation as it doesn't guarantee an optimal schedule in the combinatorial sense
    for j in range(num_jobs):
        for k in range(j + 1, num_jobs):
            solver.Add(completion_times[j] >= completion_times[k] + processing_times[j] - M * (
                    1 - solver.IntVar(0, 1, f"y_{j}_{k}")))
            solver.Add(completion_times[k] >= completion_times[j] + processing_times[k] - M * solver.IntVar(0, 1,
                                                                                                            f"y_{j}_{k}"))

    # Objective: Minimize weighted completion times
    objective = solver.Objective()
    for j in range(num_jobs):
        objective.SetCoefficient(completion_times[j], weights[j])
    objective.SetMinimization()

    solver_status = solver.Solve()

    if solver_status != pywraplp.Solver.OPTIMAL:
        raise SolverError(f"Unable to find the optimal solution for the combinatorial model, first criterion. "
                          f"{solver_status = }")

    approximate_completion_times = [c.solution_value() for c in completion_times]
    return approximate_completion_times
