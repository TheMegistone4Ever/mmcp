import codecs
import json

import numpy as np

from data_generation import generate_linear_model_data, generate_combinatorial_model_data


def generate_data_json_file(filename, num_elements=5, num_vars=10, num_jobs=10):
    """Generates a data file (JSON wrapper) with synthetic data.

    Args:
        filename (str): The name of the file to write.
        num_elements (int): The number of elements.
        num_vars (int): The number of variables in each element.
        num_jobs (int): The number of jobs.
    """

    data = {
        **generate_linear_model_data(num_elements, num_vars),
        **generate_combinatorial_model_data(num_vars, num_jobs)
    }

    # Convert numpy arrays to list for JSON serialization
    for key, value in data.items():
        if isinstance(value, np.ndarray):
            data[key] = value.tolist()
        elif isinstance(value, dict):  # Handle precedence_graph
            for inner_key, inner_value in value.items():
                if isinstance(inner_value, np.ndarray):
                    value[inner_key] = inner_value.tolist()
        elif isinstance(value, list):  # Handle "d" list with potential None and ndarray
            data[key] = [item.tolist() if isinstance(item, np.ndarray) else item for item in value]

    with codecs.open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f,
                  separators=(",", ":"),
                  sort_keys=True,
                  indent=4)

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

    print(json.dumps(format_value(value), indent=4))


if __name__ == "__main__":
    file_path = "../ui/example.json"
    generate_data_json_file(file_path)
    with open(file_path, "r") as generated:
        print_with_precision(json.load(generated))
