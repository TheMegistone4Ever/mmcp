from ortools.linear_solver import pywraplp


def solve(c, A, b, z_min, alpha):
    """
    Solves the second criterion for the first linear model.

    Args:
        c: Vector of coefficients for the objective function.
        A: Matrix of constraint coefficients.
        b: Vector of constraint bounds.
        z_min: The minimum acceptable value for the objective function.
        alpha: The expert-defined threshold.

    Returns:
        A tuple containing:
            - The optimal solution vector x.
            - The optimal objective value.
    """

    solver = pywraplp.Solver.CreateSolver("GLOP")

    num_vars = len(c)
    x = [solver.NumVar(0, solver.infinity(), f"x_{i}") for i in range(num_vars)]

    # Add constraints
    for i in range(len(b)):
        constraint = solver.Constraint(-solver.infinity(), b[i])
        for j in range(num_vars):
            constraint.SetCoefficient(x[j], A[i][j])

    # Add the expert constraint
    expert_constraint = solver.Constraint(z_min * (1 - alpha), solver.infinity())
    for i in range(num_vars):
        expert_constraint.SetCoefficient(x[i], c[i])

    # Minimize the sum of x_i
    objective = solver.Objective()
    for i in range(num_vars):
        objective.SetCoefficient(x[i], 1)
    objective.SetMinimization()

    solver.Solve()

    optimal_x = [x[i].solution_value() for i in range(num_vars)]
    optimal_objective = objective.Value()

    return optimal_x, optimal_objective
