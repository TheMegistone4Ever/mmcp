import logging

logging.basicConfig(filename=r".\logs\mmcp.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

from typing import NamedTuple, List, Dict, Any

from numpy import ndarray

from mmcp.utils import ModelType, message, Criterion


class LinearModelData(NamedTuple):
    logging.debug(f"Initialized {__name__}")
    c: ndarray = None
    A: ndarray = None
    b: ndarray = None
    d: List[ndarray] = None
    criteria: ndarray = None
    model_types: ndarray = None

    def set_model_type_for_all(self, model_types: ndarray):
        """
        Sets or updates the model_type for all elements.

        Args:
            model_types: The new model_type values.
        """
        logging.debug(f"Setting model type for all elements to {model_types}")
        self.model_types[:] = model_types

    def set_criteria_for_all(self, criteria: ndarray):
        """
        Sets or updates the criteria for all elements.

        Args:
            criteria: The new criterion values.
        """
        logging.debug(f"Setting criterion for all elements to {criteria}")
        self.criteria[:] = criteria

    def __repr__(self) -> str:
        return message("Linear Model Data", self._asdict())


class CombinatorialModelData(NamedTuple):
    logging.debug(f"Initialized {__name__}")
    processing_times: ndarray = None
    precedence_graph: Dict[int, ndarray] = None
    weights: ndarray = None

    def __repr__(self) -> str:
        return message("Combinatorial Model Data", self._asdict())


class ModelData(NamedTuple):
    logging.debug(f"Initialized {__name__}")
    c: ndarray = None
    A: ndarray = None
    b: ndarray = None
    d: List[ndarray] = None
    criteria: ndarray = None
    model_types: ndarray = None
    processing_times: ndarray = None
    precedence_graph: Dict[int, ndarray] = None
    weights: ndarray = None

    def __repr__(self) -> str:
        return message("Model Data", self._asdict())

    def set_model_type(self, element_idx: int, model_type: ModelType):
        """
        Sets or updates the model_type for a specific element.

        Args:
            element_idx: The index of the element to update.
            model_type: The new model_type value.
        """
        logging.debug(f"Setting model type for element {element_idx} to {model_type}")
        assert 0 <= element_idx < len(self.model_types), f"Invalid element index: {element_idx}"
        self.model_types[element_idx] = int(model_type)

    def set_criteria(self, element_idx: int, criterion: Criterion):
        """
        Sets or updates the criterion for a specific element.

        Args:
            element_idx: The index of the element to update.
            criterion: The new criterion value.
        """
        logging.debug(f"Setting criterion for element {element_idx} to {criterion}")
        assert 0 <= element_idx < len(self.criteria), f"Invalid element index: {element_idx}"
        self.criteria[element_idx] = int(criterion)


class SolutionData(NamedTuple):
    logging.debug(f"Initialized {__name__}")
    names: List[str] = list()
    values: List[Any] = list()

    def __repr__(self) -> str:
        return f"Solution Data:\n{"\n".join([f"{name}:\n{value}\n" for name, value in zip(self.names, self.values)])}"
