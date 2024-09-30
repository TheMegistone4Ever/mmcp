import logging

from mmcp.utils import Vars

logging.basicConfig(filename=r".\logs\mmcp.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

from ortools.linear_solver import pywraplp

from mmcp.core import SolverError


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
    logging.debug(f"Entering solve function in criterion_2.py with: "
                  f"processing_times={processing_times}, "
                  f"precedence_graph={precedence_graph}, "
                  f"initial_weights={initial_weights}, "
                  f"target_differences={target_differences}")

    num_jobs = len(processing_times) if isinstance(processing_times, list) else 1
    weights = initial_weights.copy()
    completion_times = None

    for _ in range(num_jobs):  # Limit iterations
        completion_times = solve_weighted_completion_time(processing_times, precedence_graph, weights, Vars.M)

        max_diff = 0
        for i, j, target_diff in target_differences:
            diff = abs(completion_times[i] - completion_times[j] - target_diff)
            if diff > max_diff:
                max_diff = diff

        if max_diff < Vars.tolerance:
            break

        # Adjust weights based on differences (example logic)
        for i, j, target_diff in target_differences:
            if completion_times[i] - completion_times[j] > target_diff:
                weights[i] -= Vars.dW  # Decrease weight for a job i
                weights[j] += Vars.dW  # Increase weight for a job j
            else:
                weights[i] += Vars.dW
                weights[j] -= Vars.dW

    logging.info(f"Completion times calculated: {completion_times}")
    return completion_times


def solve_weighted_completion_time(processing_times, precedence_graph, weights, M):
    """
    Helper function: Solves the weighted completion time problem using LP relaxation (similar to Criterion 1).

    Args:
        processing_times: A list of processing times for each job.
        precedence_graph: A dictionary representing the precedence graph (key: job, value: list of predecessors).
        weights: A list of weights for each job.
        M: A large constant.

    Returns:
        A list of job completion times (approximation).
    """
    logging.debug(f"Entering solve_weighted_completion_time function with: "
                  f"processing_times={processing_times}, "
                  f"precedence_graph={precedence_graph}, "
                  f"weights={weights}, M={M}")

    num_jobs = len(processing_times)
    solver = pywraplp.Solver.CreateSolver("GLOP")
    completion_times = [solver.NumVar(0, solver.infinity(), f"C_{j}") for j in range(num_jobs)]

    # Precedence constraints
    for j in range(num_jobs):
        for pred in precedence_graph.get(j, list()):
            solver.Add(completion_times[j] >= completion_times[pred] + processing_times[j])

    # Non-overlap constraints (simplified for LP relaxation)
    for j in range(num_jobs):
        for k in range(j + 1, num_jobs):
            solver.Add(completion_times[j] >= completion_times[k] + processing_times[j]
                       - M * (1 - solver.IntVar(0, 1, f"y_{j}_{k}")))
            solver.Add(completion_times[k] >= completion_times[j] + processing_times[k]
                       - M * solver.IntVar(0, 1, f"y_{j}_{k}"))

    # Objective: Minimize weighted completion times
    objective = solver.Objective()
    for j in range(num_jobs):
        objective.SetCoefficient(completion_times[j], weights[j])
    objective.SetMinimization()

    solver_status = solver.Solve()

    if solver_status != pywraplp.Solver.OPTIMAL:
        logging.error(f"Unable to find the optimal solution for the combinatorial model, second criterion. "
                      f"{solver_status=}")
        raise SolverError(f"Unable to find the optimal solution for the combinatorial model, second criterion. "
                          f"{solver_status=}")

    completion_times_values = [c.solution_value() for c in completion_times]
    logging.debug(f"Completion times calculated (inner function): {completion_times_values}")
    return completion_times_values
