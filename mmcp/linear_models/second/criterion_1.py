from ortools.linear_solver import pywraplp


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

    solver.Solve()

    optimal_x = [x[i].solution_value() for i in range(num_vars)]
    optimal_objective = objective.Value()

    return optimal_x, optimal_objective
