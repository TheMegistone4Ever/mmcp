import numpy as np
import yaml


def numpy_array_representer(dumper, data):
    """Representer for NumPy arrays."""
    return dumper.represent_list(data.tolist())


yaml.add_representer(np.ndarray, numpy_array_representer)


def numpy_array_constructor(loader, node):
    """Constructor for NumPy arrays from YAML."""
    value = loader.construct_sequence(node)
    return np.array(value)


yaml.add_constructor('tag:yaml.org,2002:python/object/apply:numpy.ndarray', numpy_array_constructor)


def parse_mmcp_file(filename):
    """
    Parses an MMCF file (YAML wrapper) and extracts the data.

    Args:
        filename: The path to the MMCF file.

    Returns:
        A dictionary containing the parsed data.
    """

    with open(filename, 'r') as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
            return {}

    return data
