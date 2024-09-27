from typing import NamedTuple, List, Dict, Any

from numpy import ndarray

from mmcp.utils import with_precision
from mmcp.utils.ModelType import ModelType

message = lambda name, dictionary: f"{name}:\n{with_precision(dictionary)}"


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

    def set_model_type(self, element_index: int, model_type: str):
        """
        Sets or updates the model_type for a specific element.

        Args:
            element_index: The index of the element to update.
            model_type: The new model_type value.
        """

        assert 0 <= element_index < len(self.model_types), f"Invalid element index: {element_index}"

        if model_type == "Linear Model 1":
            model_type = ModelType.LINEAR_MODEL_1
        elif model_type == "Linear Model 2":
            model_type = ModelType.LINEAR_MODEL_2
        elif model_type == "Combinatorial Model":
            model_type = ModelType.COMBINATORIAL_MODEL
        else:
            raise ValueError(f"Invalid model type: {model_type}")

        self.model_types[element_index] = int(model_type)

    def __repr__(self) -> str:
        return message("Model Data", self._asdict())


class SolutionData(NamedTuple):
    names: List[str] = list()
    values: List[Any] = list()

    def __repr__(self) -> str:
        return f"Solution Data:\n{"\n".join([f"{name}: {value}" for name, value in zip(self.names, self.values)])}"
