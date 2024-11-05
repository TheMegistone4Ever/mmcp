import logging

from .config import Vars, Criterion, ModelType
from .functions import ith_data, measure_execution_time, is_valid_combination
from .outs import with_precision, message

logging.basicConfig(filename=r".\logs\mmcp.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

logging.debug(f"Initialized {__name__}")

__all__ = [
    "Vars",
    "Criterion",
    "ModelType",
    "with_precision",
    "message",
    "ith_data",
    "measure_execution_time",
    "is_valid_combination",
]
