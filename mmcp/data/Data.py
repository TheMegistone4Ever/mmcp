from typing import NamedTuple, List, Dict, Any

from numpy import ndarray

from mmcp.utils import with_precision

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

    # setters

    def set_c(self, c: ndarray):
        self.c = c

    def set_A(self, A: ndarray):
        self.A = A

    def set_b(self, b: ndarray):
        self.b = b

    def set_d(self, d: List[ndarray]):
        self.d = d

    def set_model_types(self, model_types: ndarray):
        self.model_types = model_types

    def set_processing_times(self, processing_times: ndarray):
        self.processing_times = processing_times

    def set_precedence_graph(self, precedence_graph: Dict[int, ndarray]):
        self.precedence_graph = precedence_graph

    def set_weights(self, weights: ndarray):
        self.weights = weights

    def __repr__(self) -> str:
        return message("Model Data", self._asdict())


class SolutionData(NamedTuple):
    names: List[str] = []
    values: List[Any] = []

    def __repr__(self) -> str:
        return f"Solution Data:\n{"\n".join([f"{name}: {value}" for name, value in zip(self.names, self.values)])}"
