import logging

logging.basicConfig(filename=r".\logs\mmcp.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

logging.debug(f"Initialized {__name__}")

from .exception import (DataParsingError, DataValidationError, ModelTypeError, CriterionError, SolverError,
                        ConfigurationError, FileSavingError)
from .model import Model
from .solver import Solver

__all__ = [
    "DataParsingError",
    "DataValidationError",
    "ModelTypeError",
    "CriterionError",
    "SolverError",
    "ConfigurationError",
    "FileSavingError",
    "Model",
    "Solver",
]
