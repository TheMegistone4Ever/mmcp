from mmcp import lm, cm
from mmcp.core import Criterion, Model
from mmcp.utils import Vars, ModelType


class Solver:
    def __init__(self, data, model_type: ModelType, criterion_type: str):
        self.data = data
        self.model = self._create_model(model_type)
        self.criterion = self._create_criterion(criterion_type)

    @staticmethod
    def _create_model(model_type: ModelType) -> Model:
        if model_type == ModelType.LINEAR_MODEL_1:
            return LinearModel1()
        elif model_type == ModelType.LINEAR_MODEL_2:
            return LinearModel2()
        elif model_type == ModelType.COMBINATORIAL_MODEL:
            return CombinatorialModel()
        elif model_type == ModelType.LINEAR_MODEL_3:  # TODO: Implement Linear Model 3
            return LinearModel3()
        else:
            raise ValueError(f"Invalid model type: {model_type}")

    @staticmethod
    def _create_criterion(criterion_type: str) -> Criterion:
        if criterion_type == "Criterion 1":
            return Criterion1()
        elif criterion_type == "Criterion 2":
            return Criterion2()
        elif criterion_type == "Criterion 3":
            return Criterion3()
        else:
            raise ValueError(f"Invalid criterion type: {criterion_type}")

    def solve(self):
        return self.criterion.apply(self.model, self.data)


class LinearModel1(Model):
    def solve(self, criterion: Criterion, data, **kwargs):
        if isinstance(criterion, Criterion1):
            return lm.first.criterion_1.solve(data.c, data.A, data.b, Vars.M)
        elif isinstance(criterion, Criterion2):
            return lm.first.criterion_2.solve(data.c, data.A, data.b, Vars.z_min, Vars.alpha)
        elif isinstance(criterion, Criterion3):
            return lm.first.criterion_3.solve(data.c, data.A, data.b, Vars.weights)
        else:
            raise ValueError(f"Unsupported criterion for Linear Model 1: {type(criterion)}")


class LinearModel2(Model):
    def solve(self, criterion: Criterion, data, **kwargs):
        if isinstance(criterion, Criterion1):
            return lm.second.criterion_1.solve(data.c, data.A, data.b, data.d, Vars.M)
        elif isinstance(criterion, Criterion2):
            return lm.second.criterion_2.solve(data.c, data.A, data.b, data.d, Vars.z_min, Vars.alpha)
        elif isinstance(criterion, Criterion3):
            return lm.second.criterion_3.solve(data.c, data.A, data.b, data.d, Vars.weights)
        else:
            raise ValueError(f"Unsupported criterion for Linear Model 2: {type(criterion)}")


class LinearModel3(Model):
    def solve(self, criterion: Criterion, data, **kwargs):
        if isinstance(criterion, Criterion1):
            return lm.third.connected_model.solve_connected_model(data.c, data.A, data.b, data.d, data.model_types,
                                                                  Vars.beta)
        else:
            raise ValueError(f"Unsupported criterion for Linear Model 3: {type(criterion)}")


class CombinatorialModel(Model):
    def solve(self, criterion: Criterion, data, **kwargs):
        if isinstance(criterion, Criterion1):
            return cm.first.criterion_1.solve(data.processing_times, data.precedence_graph, data.weights, Vars.M)
        elif isinstance(criterion, Criterion2):
            return cm.first.criterion_2.solve(data.processing_times, data.precedence_graph, data.weights,
                                              Vars.target_difference)
        else:
            raise ValueError(f"Unsupported criterion for Combinatorial Model: {type(criterion)}")


class Criterion1(Criterion):
    def apply(self, model: Model, *args, **kwargs):
        return model.solve(self, *args, **kwargs)


class Criterion2(Criterion):
    def apply(self, model: Model, *args, **kwargs):
        return model.solve(self, *args, **kwargs)


class Criterion3(Criterion):
    def apply(self, model: Model, *args, **kwargs):
        return model.solve(self, *args, **kwargs)
