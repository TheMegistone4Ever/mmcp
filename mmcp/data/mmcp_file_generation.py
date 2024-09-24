import yaml

from data_generation import generate_linear_model_data, generate_combinatorial_model_data


# noinspection PyDictCreation
def generate_mmcp_file(filename, num_elements=5, num_vars=10, num_jobs=10):
    """Generates an example MMCF file (YAML wrapper) with synthetic data.

    Args:
        filename (str): The name of the file to write.
        num_elements (int): The number of elements in the MMCF file.
        num_vars (int): The number of variables in each element.
        num_jobs (int): The number of jobs in the combinatorial model.
    """

    data = {
        **generate_linear_model_data(num_elements, num_vars),
        **generate_combinatorial_model_data(num_vars, num_jobs)
    }

    with open(filename, "w") as f:
        yaml.dump(data, f)

    print(f"Generated MMCF file: {filename}\nData:\n{data}")


# Example usage:
if __name__ == "__main__":
    generate_mmcp_file("../ui/example.mmcp")
