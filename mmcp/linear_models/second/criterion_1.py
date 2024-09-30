import logging

logging.basicConfig(filename=r".\logs\mmcp.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

from ortools.linear_solver import pywraplp

from mmcp.core import SolverError


def solve(c, A, b, d, M):
    """
    Solves the first criterion for the second linear model.

    Args:
        c: Vector of coefficients for the objective function.
        A: Matrix of constraint coefficients.
        b: Vector of constraint bounds.
        d: Vector of private resources for each element.
        M: A large constant.

    Returns:
        A tuple containing:
            - The optimal solution vector x.
            - The optimal objective value.
    """
    logging.debug(f"Entering solve function in criterion_1.py (linear_models/second) with: "
                  f"c={c}, A={A}, b={b}, d={d}, M={M}")

    solver = pywraplp.Solver.CreateSolver("GLOP")

    num_vars = len(c)
    x = [solver.NumVar(0, solver.infinity(), f"x_{i}") for i in range(num_vars)]

    # Add constraints
    for i in range(len(b)):
        constraint = solver.Constraint(-solver.infinity(), b[i])
        for j in range(num_vars):
            constraint.SetCoefficient(x[j], A[i][j])

    # Solve for z_max
    objective_max = solver.Objective()
    for i in range(num_vars):
        objective_max.SetCoefficient(x[i], c[i] + d[i])  # Include private resources in objective
    objective_max.SetMaximization()
    solver.Solve()
    z_max = objective_max.Value()

    # Solve with the additional constraint z >= z_max
    objective = solver.Objective()
    for i in range(num_vars):
        objective.SetCoefficient(x[i], 1)  # Minimize the sum of x_i
    objective.SetMinimization()

    z_constraint = solver.Constraint(z_max, solver.infinity())
    for i in range(num_vars):
        z_constraint.SetCoefficient(x[i], c[i] + d[i])

    solver_status = solver.Solve()

    if solver_status != pywraplp.Solver.OPTIMAL:
        logging.error(f"Unable to find the optimal solution for the second linear model, first criterion. "
                      f"{solver_status=}")
        raise SolverError(f"Unable to find the optimal solution for the second linear model, first criterion. "
                          f"{solver_status=}")

    optimal_x = [x[i].solution_value() for i in range(num_vars)]
    optimal_objective = objective.Value()
    logging.info(f"Optimal solution found for the second linear model, first criterion: "
                 f"x={optimal_x}, objective={optimal_objective}")

    return optimal_x, optimal_objective
