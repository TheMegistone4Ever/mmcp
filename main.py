from mmcp import lm, cm
from mmcp.data import generate_linear_model_data, generate_combinatorial_model_data


def main():
    linear_data = generate_linear_model_data()
    combinatorial_data = generate_combinatorial_model_data()
    first_linear_data = {k: list(v)[0] for k, v in linear_data._asdict().items()}
    first_combinatorial_data = {k: list(v)[0] for k, v in combinatorial_data._asdict().items()}
    first_combinatorial_data["precedence_graph"] = {1: list()}

    print("Linear model data for the first element:")
    for name, values in first_linear_data.items():
        print(f"{name=}:\n{values}\n")

    optimal_x, optimal_objective = lm.first.criterion_1.solve(**dict(list(first_linear_data.items())[:3]), M=1000)
    print(f"Optimal x for the first criterion of the first linear model: {optimal_x}")
    print(f"Optimal objective value for the first criterion of the first linear model: {optimal_objective}\n")

    print("Combinatorial model data for the first element:")
    for name, values in first_combinatorial_data.items():
        print(f"{name=}:\n{values}\n")

    approximate_completion_times = cm.first.criterion_1.solve(**first_combinatorial_data, M=1000)
    print(f"Approximate completion times for the combinatorial model: {approximate_completion_times}")


# TODO: Error Handling, use: class ...(Exception): ...
# TODO: Logging, use: logging.basicConfig(...)
# TODO: Change data generation to this: (Element 1 data), (Element 2 data), ...

if __name__ == "__main__":
    main()
