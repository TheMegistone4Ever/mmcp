from typing import NamedTuple, List, Dict, Any

from numpy import ndarray

from mmcp.utils import ModelType, message


class LinearModelData(NamedTuple):
    c: ndarray = None
    A: ndarray = None
    b: ndarray = None
    d: List[ndarray] = None
    model_types: ndarray = None

    def __repr__(self) -> str:
        return message("Linear Model Data", self._asdict())


class CombinatorialModelData(NamedTuple):
    processing_times: ndarray = None
    precedence_graph: Dict[int, ndarray] = None
    weights: ndarray = None

    def __repr__(self) -> str:
        return message("Combinatorial Model Data", self._asdict())


class ModelData(NamedTuple):
    c: ndarray = None
    A: ndarray = None
    b: ndarray = None
    d: List[ndarray] = None
    model_types: ndarray = None
    processing_times: ndarray = None
    precedence_graph: Dict[int, ndarray] = None
    weights: ndarray = None

    def set_model_type(self, element_index: int, model_type: ModelType):
        """
        Sets or updates the model_type for a specific element.

        Args:
            element_index: The index of the element to update.
            model_type: The new model_type value.
        """

        assert 0 <= element_index < len(self.model_types), f"Invalid element index: {element_index}"
        self.model_types[element_index] = int(model_type)

    def __repr__(self) -> str:
        return message("Model Data", self._asdict())


class SolutionData(NamedTuple):
    values: List[Any] = list()

    def __repr__(self) -> str:
        return f"Solution Data:\n{"\n".join([f"Element №{i + 1}:\n{value}\n" for i, value in enumerate(self.values)])}"
