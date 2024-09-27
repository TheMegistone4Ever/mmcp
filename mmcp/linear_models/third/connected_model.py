from ortools.linear_solver import pywraplp


def solve_connected_model(c_list, A_list, b_list, d_list, model_types, beta):
    """
    Solves the connected model for the third linear model.

    Args:
        c_list: List of coefficient vectors for the objective functions of each element.
        A_list: List of constraint matrices for each element.
        b_list: List of constraint bound vectors for each element.
        d_list: List of private resource vectors for each element (None if an element uses the first linear model).
        model_types: List indicating the type of model for each element (1 for the first linear model, 2 for the second).
        beta: The parameter controlling the compromise between the center and the elements.

    Returns:
        A list of optimal solution vectors for each element.
    """

    solver = pywraplp.Solver.CreateSolver("GLOP")

    num_elements = len(c_list)
    x_list = list()
    for i in range(num_elements):
        num_vars = len(c_list[i])
        x_list.append([solver.NumVar(0, solver.infinity(), f"x_{i}_{j}") for j in range(num_vars)])

    # Add constraints for each element
    for i in range(num_elements):
        for j in range(len(b_list[i])):
            constraint = solver.Constraint(-solver.infinity(), b_list[i][j])
            for k in range(len(x_list[i])):
                constraint.SetCoefficient(x_list[i][k], A_list[i][j][k])

    # Add connecting constraints (a sum of corresponding variables across elements is bounded)
    for j in range(len(c_list[0])):  # Assuming all elements have the same number of variables
        connecting_constraint = solver.Constraint(0, solver.infinity())  # Adjust bounds as needed
        for i in range(num_elements):
            connecting_constraint.SetCoefficient(x_list[i][j], 1)

            # Define the objective function (compromise between center and elements)
    objective = solver.Objective()
    for i in range(num_elements):
        for j in range(len(x_list[i])):
            if model_types[i] == 1:
                objective.SetCoefficient(x_list[i][j], beta * c_list[i][j])
            elif model_types[i] == 2:
                objective.SetCoefficient(x_list[i][j], beta * c_list[i][j] + (1 - beta) * d_list[i][j])
    objective.SetMaximization()  # or SetMinimization() depending on the problem

    solver.Solve()

    optimal_solutions = [[x.solution_value() for x in element_x] for element_x in x_list]

    return optimal_solutions
