import logging

logging.basicConfig(filename=r"..\..\logs\mmcp.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

from codecs import open as codecs_open
from json import dump, load

from numpy import ndarray

from mmcp.core import FileSavingError
from mmcp.data import generate_model_data
from mmcp.utils import with_precision


# noinspection PyProtectedMember
def generate_data_json_file(filename, num_elements=5, num_vars=10, num_jobs=10, data=None):
    """
    Generates a data file (JSON wrapper) with synthetic data.

    Args:
        filename (str): The name of the file to write.
        num_elements (int): The number of elements.
        num_vars (int): The number of variables in each element.
        num_jobs (int): The number of jobs.
        data (dict): The data to write to the file. If None, synthetic data will be generated.
    """
    logging.debug(f"Entering generate_data_json_file with filename={filename}, num_elements={num_elements}, "
                  f"num_vars={num_vars}, num_jobs={num_jobs}, data={data}")

    if data is None:
        data = generate_model_data(num_elements, num_vars, num_jobs)

    dict_data = data._asdict()

    # Convert numpy arrays to list for JSON serialization
    for key, value in dict_data.items():
        if isinstance(value, ndarray):
            dict_data[key] = value.tolist()
        elif isinstance(value, dict):  # Handle precedence_graph
            for inner_key, inner_value in value.items():
                if isinstance(inner_value, ndarray):
                    value[inner_key] = inner_value.tolist()
        elif isinstance(value, list):  # Handle "d" list with potential None and ndarray
            dict_data[key] = [item.tolist() if isinstance(item, ndarray) else item for item in value]

    with codecs_open(filename, "w", encoding="utf-8") as f:
        try:
            dump(dict_data, f, separators=(",", ":"), indent=2)
            logging.info(f"Generated data file (JSON): {filename}")
        except OSError as e:
            logging.exception(f"Error saving data to JSON file: {e}")
            raise FileSavingError(f"Error saving data to JSON file: {e}") from e

    print(f"Generated data file (JSON): {filename}...")


if __name__ == "__main__":
    file_path = "../ui/example.json"
    generate_data_json_file(file_path)
    with open(file_path, "r") as generated:
        print(with_precision(load(generated)))
