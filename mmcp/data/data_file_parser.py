import codecs
import json

import numpy as np


def parse_data_json_file(filename):
    """Parses a data JSON file and reconstructs NumPy arrays."""
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Convert lists back to NumPy arrays, handling 'd' key
    for key, value in data.items():
        if isinstance(value, list):
            if key == 'd':  # Special handling for 'd' key
                data[key] = [np.array(item) if item is not None else None for item in value]
            else:
                data[key] = np.array(value)
        elif isinstance(value, dict):  # Handle precedence_graph
            for inner_key, inner_value in value.items():
                if isinstance(inner_value, list):
                    value[inner_key] = np.array(inner_value)

    return data


if __name__ == "__main__":
    file_path = "../ui/example.json"
    parsed_data = parse_data_json_file(file_path)
    print("Parsed Data (with NumPy arrays):")
    np.set_printoptions(precision=2, suppress=True)
    print(parsed_data)
    np.set_printoptions()
