from ..utils.logger_setup import LOGGER


class BaseCustomError(Exception):
    """
    Base class for all custom exceptions.
    """
    LOGGER.debug(f"Initialized {__name__}")


class DataParsingError(BaseCustomError):
    """
    Raised when there"s an error parsing the data file.

    This exception is triggered when the input data file cannot be
    correctly parsed, typically due to formatting issues or corrupted content.
    """
    LOGGER.debug(f"Initialized {__name__}")


class DataValidationError(BaseCustomError):
    """
    Raised when the parsed data doesn't meet validation criteria.

    This occurs when the parsed data fails to meet the required structure
    or contains invalid values according to the validation logic.
    """
    LOGGER.debug(f"Initialized {__name__}")


class ModelTypeError(BaseCustomError):
    """
    Raised when an invalid model type is specified.

    This exception is used when the provided model type doesn't match
    any of the recognized or supported model types.
    """
    LOGGER.debug(f"Initialized {__name__}")


class CriterionError(BaseCustomError):
    """
    Raised when an invalid criterion is specified.

    This exception is thrown when a given criterion for solving
    the optimization problem is invalid or unrecognized.
    """
    LOGGER.debug(f"Initialized {__name__}")


class SolverError(BaseCustomError):
    """
    Raised when an error occurs during solving the optimization problem.

    This occurs if the solver encounters an issue, such as
    convergence problems, numerical instability, or invalid inputs.
    """
    LOGGER.debug(f"Initialized {__name__}")


class ConfigurationError(BaseCustomError):
    """
    Raised when an error occurs during element configuration.

    Thrown when the system or components can"t be configured properly
    due to missing parameters, incorrect settings, or dependency issues.
    """
    LOGGER.debug(f"Initialized {__name__}")


class FileSavingError(BaseCustomError):
    """
    Raised when an error occurs during saving the solution to a file.

    This exception is triggered if the system fails to save the results
    to a file, due to I/O errors, permission issues, or invalid paths.
    """
    LOGGER.debug(f"Initialized {__name__}")
