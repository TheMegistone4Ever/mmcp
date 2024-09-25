from codecs import open as codecs_open
from json import load

from PyQt5.QtWidgets import QMessageBox
from numpy import array, set_printoptions

type_error = lambda key, expected_type: f"❌ Incorrect data type for '{key}'! Expected {expected_type}."


def parse_data_json_file(filename):
    """Parses a data JSON file and reconstructs NumPy arrays.

    Performs checks for data correctness, particularly for linear programming:
      - Presence of required keys.
      - Correct data types and dimensions.
      - Positivity of A, b, and d (element-wise).
      - Consistent dimensions across data elements.

    Raises:
        SystemExit: If data validation fails, displaying a QMessageBox critical error.
    """
    with codecs_open(filename, 'r', encoding='utf-8') as f:
        data = load(f)

    try:
        # Check if required keys exist
        for key in ["c", "A", "b", "d", "model_types", "processing_times", "precedence_graph", "weights"]:
            if key not in data:
                raise ValueError(f"Missing key '{key}' in the JSON data.")

        # --- Dimension and Type Checks ---
        num_elements = len(data["c"])
        num_vars = len(data["c"][0])  # Assuming c is a list of lists, num_vars is consistent

        if not all(len(item) == num_vars for item in data["c"]):
            raise ValueError("Inconsistent dimensions in 'c'. All elements should have the same number of variables.")

        if not all(len(item) == num_vars for item in data["A"]):
            raise ValueError(
                "Inconsistent dimensions in 'A'. The number of sub-lists should match the number of variables."
            )
        if not all(len(subitem) == num_vars for item in data["A"] for subitem in item):
            raise ValueError(
                "Inconsistent dimensions in 'A'. Sub-lists should have dimensions matching the number of variables."
            )

        if not len(data["b"]) == num_elements or not all(len(item) == num_vars for item in data["b"]):
            raise ValueError("Inconsistent dimensions in 'b'. Should match the number of elements and variables.")

        if not len(data["d"]) == num_elements:
            raise ValueError("Inconsistent dimensions in 'd'. Should match the number of elements.")

        if not len(data["model_types"]) == num_elements:
            raise ValueError("Inconsistent dimensions in 'model_types'. Should match the number of elements.")

        if not len(data["processing_times"]) == num_vars:
            raise ValueError("Inconsistent dimensions in 'processing_times'. Should match the number of variables.")

        if not len(data["weights"]) == num_vars:
            raise ValueError("Inconsistent dimensions in 'weights'. Should match the number of variables.")
        if not all(len(item) == num_vars for item in data["weights"]):
            raise ValueError(
                "Inconsistent dimensions in 'weights'. The number of sub-lists should match the number of variables."
            )

        # --- Positivity Checks ---
        if not all(item >= 0 for sub_sub_list in data["A"] for sub_list in sub_sub_list for item in sub_list):
            raise ValueError("Matrix 'A' should have all non-negative elements.")
        if not all(item >= 0 for sublist in data["b"] for item in sublist):
            raise ValueError("Vector 'b' should have all non-negative elements.")
        if not all(all(item >= 0 for item in sublist) if sublist is not None else True for sublist in data["d"]):
            raise ValueError("Vector 'd' should have all non-negative elements.")

        # --- Data Type Checks ---
        if not isinstance(data["c"], list) or not all(isinstance(item, list) for item in data["c"]) or not all(
                isinstance(subitem, (int, float)) for item in data["c"] for subitem in item):
            raise TypeError(type_error("c", "list of lists of numbers"))
        if not isinstance(data["A"], list) or not all(
                isinstance(item, list) and all(isinstance(subitem, list) for subitem in item)
                for item in data["A"]
        ) or not all(
            isinstance(sub_sub_item, (int, float)) for sub_list in data["A"] for item in sub_list for sub_sub_item in
            item):
            raise TypeError(type_error("A", "list of lists of lists of numbers"))
        if not isinstance(data["b"], list) or not all(isinstance(item, list) for item in data["b"]) or not all(
                isinstance(subitem, (int, float)) for item in data["b"] for subitem in item):
            raise TypeError(type_error("b", "list of lists of numbers"))
        if not isinstance(data["d"], list) or not all(
                isinstance(item, (list, type(None))) for item in data["d"]) or not all(
            all(isinstance(subitem, (int, float)) for subitem in item) if item is not None else True for item in
            data["d"]):
            raise TypeError(type_error("d", "list of numbers (or None)"))
        if not isinstance(data["model_types"], list) or not all(isinstance(item, int) for item in data["model_types"]):
            raise TypeError(type_error("model_types", "list of integers"))
        if not isinstance(data["processing_times"], list) or not all(
                isinstance(item, (int, float)) for item in data["processing_times"]):
            raise TypeError(type_error("processing_times", "NumPy array of numbers"))
        if not isinstance(data["precedence_graph"], dict):
            raise TypeError(type_error("precedence_graph", "dictionary"))
        for key, value in data["precedence_graph"].items():
            if not isinstance(value, list) or not all(isinstance(item, int) for item in value):
                raise TypeError(type_error(f"precedence_graph['{key}']", "list of integers"))
        if not isinstance(data["weights"], list) or not all(
                isinstance(item, (int, float)) for sub_list in data["weights"] for item in sub_list):
            raise TypeError(type_error("weights", "NumPy array of numbers"))

        # --- Convert lists to NumPy arrays ---
        data["c"] = array(data["c"])
        data["A"] = array(data["A"])
        data["b"] = array(data["b"])
        data["d"] = array(data["d"], dtype=object)
        data["processing_times"] = array(data["processing_times"])
        for key, value in data["precedence_graph"].items():
            data["precedence_graph"][key] = array(value)
        data["weights"] = array(data["weights"])

        return data

    except (ValueError, TypeError, KeyError) as e:
        QMessageBox.critical(None, "Please review the file carefully.", f"Error parsing data file: {e}")


if __name__ == "__main__":
    file_path = "../ui/example.json"
    parsed_data = parse_data_json_file(file_path)
    print("Parsed Data (with NumPy arrays):")
    set_printoptions(precision=2, suppress=True)
    print(parsed_data)
    set_printoptions()
