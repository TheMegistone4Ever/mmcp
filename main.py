from mmcp import *


def main():
    # Generate data for linear models
    c_list, A_list, b_list, d_list, model_types = generate_linear_model_data()

    # Generate data for the combinatorial model
    processing_times, precedence_graph, weights = generate_combinatorial_model_data()

    # Example: Solve the first criterion for the first linear model for the first element
    optimal_x, optimal_objective = lm.first.criterion_1.solve(c_list[0], A_list[0], b_list[0], M=1000)

    # Example: Solve the first criterion for the combinatorial model
    approximate_completion_times = cm.first.criterion_1.solve(
        processing_times, precedence_graph, weights, M=1000
    )

    # print input data
    for name, values in zip(["c_list", "A_list", "b_list", "d_list", "model_types"],
                            [c_list, A_list, b_list, d_list, model_types]):
        print(f"{name=}:\n{values}\n")

    print("Optimal x for the first criterion of the first linear model:")
    print(optimal_x)

    print("Optimal objective value for the first criterion of the first linear model:")
    print(optimal_objective)

    print("Approximate completion times for the combinatorial model:")
    print(approximate_completion_times)


if __name__ == "__main__":
    main()
