from ortools.linear_solver import pywraplp

from mmcp.core import SolverError
from ...utils.logger_setup import LOGGER


def solve(c, A, b, weights):
    """
    Solves the third criterion for the first linear model using an iterative procedure.

    Args:
        c: Vector of coefficients for the objective function.
        A: Matrix of constraint coefficients.
        b: Vector of constraint bounds.
        weights: Vector of weights representing the importance of each element.

    Returns:
        A tuple containing:
            - The optimal solution vector x.
            - The optimal objective value.
    """
    LOGGER.debug(f"Entering solve function in criterion_3.py (linear_models/first) with: "
                 f"c={c}, A={A}, b={b}, weights={weights}")

    solver = pywraplp.Solver.CreateSolver("GLOP")

    num_vars = len(c)
    x = [solver.NumVar(0, solver.infinity(), f"x_{i}") for i in range(num_vars)]

    # Add constraints
    for i in range(len(b)):
        constraint = solver.Constraint(-solver.infinity(), b[i])
        for j in range(num_vars):
            constraint.SetCoefficient(x[j], A[i][j])

    # Iterative procedure
    tolerance = 1e-6  # Define a tolerance for convergence
    max_iterations = 100

    z_prev = 0

    objective = solver.Objective()
    for iteration in range(max_iterations):
        objective = solver.Objective()
        for i in range(num_vars):
            objective.SetCoefficient(x[i], weights[i] * c[i])
        objective.SetMaximization()

        solver_status = solver.Solve()

        if solver_status != pywraplp.Solver.OPTIMAL:
            LOGGER.error(f"Unable to find the optimal solution for the first linear model, third criterion. "
                         f"{solver_status=}, {iteration=}")
            raise SolverError(f"Unable to find the optimal solution for the first linear model, third criterion. "
                              f"{solver_status=}, {iteration=}")

        z_current = objective.Value()

        if abs(z_current - z_prev) < tolerance:
            break

        z_prev = z_current
        # Update weights based on the current solution (implementation depends on the specific update rule)
        weights = update_weights(weights, x)

    optimal_x = [x[i].solution_value() for i in range(num_vars)]
    optimal_objective = objective.Value()
    LOGGER.info(f"Optimal solution found for the first linear model, third criterion: "
                f"x={optimal_x}, objective={optimal_objective}")

    return optimal_x, optimal_objective


def update_weights(weights, x):
    """
    Update the weights based on the current solution.

    Args:
        weights: Vector of weights representing the importance of each element.
        x: Vector of decision variables.

    Returns:
        Updated weights.
    """
    LOGGER.debug(f"Updating weights in criterion_3.py (linear_models/first) with weights={weights}, x={x}")

    # Update weights based on the current solution
    weights = [w * xi.solution_value() for w, xi in zip(weights, x)]

    # normalization to not blow up the weights
    total = sum(weights)
    weights = [w / total for w in weights if total != 0]
    LOGGER.debug(f"Updated weights: {weights}")

    return weights
