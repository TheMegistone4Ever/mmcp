import logging

logging.basicConfig(filename=r"..\..\logs\mmcp.log", level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

from json import dumps

from numpy import ndarray, number

logging.debug(f"Initialized {__name__}")


def with_precision(value, precision=2) -> str:
    """
    Prints the data with specified precision for numeric values.

    Args:
        value: The value to print.
        precision (int): The number of decimal places to print.
    """
    logging.debug(f"Formatting value with precision: {precision}")

    def format_value(val):
        if isinstance(val, (float, int)):
            return f"{val:.{precision}f}"
        elif isinstance(val, (ndarray, number)):
            return format_value(val.tolist())
        elif isinstance(val, list):
            return [format_value(item) for item in val]
        elif isinstance(val, dict):
            return {k: format_value(v) for k, v in val.items()}
        else:
            return val

    return dumps(format_value(value), indent=2)


message = lambda name, dictionary: f"{name}:\n{with_precision(dictionary)}"
