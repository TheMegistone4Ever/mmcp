from codecs import open as codecs_open
from json import dump, dumps, load

from numpy import ndarray

from mmcp.data import generate_linear_model_data, generate_combinatorial_model_data


def generate_data_json_file(filename, num_elements=5, num_vars=10, num_jobs=10, data=None):
    """Generates a data file (JSON wrapper) with synthetic data.

    Args:
        filename (str): The name of the file to write.
        num_elements (int): The number of elements.
        num_vars (int): The number of variables in each element.
        num_jobs (int): The number of jobs.
        data (dict): The data to write to the file. If None, synthetic data will be generated.
    """

    if data is None:
        data = {
            **generate_linear_model_data(num_elements, num_vars),
            **generate_combinatorial_model_data(num_vars, num_jobs)
        }

    # Convert numpy arrays to list for JSON serialization
    for key, value in data.items():
        if isinstance(value, ndarray):
            data[key] = value.tolist()
        elif isinstance(value, dict):  # Handle precedence_graph
            for inner_key, inner_value in value.items():
                if isinstance(inner_value, ndarray):
                    value[inner_key] = inner_value.tolist()
        elif isinstance(value, list):  # Handle "d" list with potential None and ndarray
            data[key] = [item.tolist() if isinstance(item, ndarray) else item for item in value]

    with codecs_open(filename, "w", encoding="utf-8") as f:
        dump(data, f, separators=(",", ":"), sort_keys=True, indent=2)

    print(f"Generated data file (JSON): {filename}...")


def print_with_precision(value, precision=2):
    """Prints the data with specified precision for numeric values.
    
    Args:
        value: The value to print.
        precision (int): The number of decimal places to print.
    """

    def format_value(val):
        if isinstance(val, (float, int)):
            return f"{val:.{precision}f}"
        elif isinstance(val, list):
            return [format_value(item) for item in val]
        elif isinstance(val, dict):
            return {k: format_value(v) for k, v in val.items()}
        else:
            return val

    print(dumps(format_value(value), indent=4))


if __name__ == "__main__":
    file_path = "../ui/example.json"
    generate_data_json_file(file_path)
    with open(file_path, "r") as generated:
        print_with_precision(load(generated))
