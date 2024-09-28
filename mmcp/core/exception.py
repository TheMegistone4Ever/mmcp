class BaseCustomError(Exception):
    """
    Base class for all custom exceptions.
    """


class DataParsingError(BaseCustomError):
    """
    Raised when there's an error parsing the data file.

    This exception is triggered when the input data file cannot be
    correctly parsed, typically due to formatting issues or corrupted content.
    """


class DataValidationError(BaseCustomError):
    """
    Raised when the parsed data doesn't meet validation criteria.

    This occurs when the parsed data fails to meet the required structure
    or contains invalid values according to the validation logic.
    """


class ModelTypeError(BaseCustomError):
    """
    Raised when an invalid model type is specified.

    This exception is used when the provided model type doesn't match
    any of the recognized or supported model types.
    """


class CriterionError(BaseCustomError):
    """
    Raised when an invalid criterion is specified.

    This exception is thrown when a given criterion for solving
    the optimization problem is invalid or unrecognized.
    """


class SolverError(BaseCustomError):
    """
    Raised when an error occurs during solving the optimization problem.

    This occurs if the solver encounters an issue, such as
    convergence problems, numerical instability, or invalid inputs.
    """


class ConfigurationError(BaseCustomError):
    """
    Raised when an error occurs during element configuration.

    Thrown when the system or components can't be configured properly
    due to missing parameters, incorrect settings, or dependency issues.
    """


class FileSavingError(BaseCustomError):
    """
    Raised when an error occurs during saving the solution to a file.

    This exception is triggered if the system fails to save the results
    to a file, due to I/O errors, permission issues, or invalid paths.
    """
