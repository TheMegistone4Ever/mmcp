from json import dumps

from numpy import ndarray


def with_precision(value, precision=2) -> str:
    """
    Prints the data with specified precision for numeric values.

    Args:
        value: The value to print.
        precision (int): The number of decimal places to print.
    """

    def format_value(val):
        if isinstance(val, (float, int)):
            return f"{val:.{precision}f}"
        elif isinstance(val, ndarray):
            return format_value(val.tolist())
        elif isinstance(val, list):
            return [format_value(item) for item in val]
        elif isinstance(val, dict):
            return {k: format_value(v) for k, v in val.items()}
        else:
            return val

    return dumps(format_value(value), indent=2)
