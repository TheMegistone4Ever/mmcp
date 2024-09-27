from mmcp import lm, cm
from mmcp.core import Model
from mmcp.utils import Vars, ModelType, Criterion


class Solver:
    def __init__(self, data, model_type: ModelType, criterion_type: Criterion):
        self.data = data
        self.model = self._create_model(model_type)
        self.criterion_type = criterion_type

    @staticmethod
    def _create_model(model_type: ModelType) -> Model:
        if model_type == ModelType.LINEAR_MODEL_1:
            return LinearModel1()
        elif model_type == ModelType.LINEAR_MODEL_2:
            return LinearModel2()
        elif model_type == ModelType.LINEAR_MODEL_3:
            return LinearModel3()
        elif model_type == ModelType.COMBINATORIAL_MODEL:
            return CombinatorialModel()
        else:
            raise ValueError(f"Invalid model type: {model_type}")

    def solve(self):
        return self.model.solve(self.criterion_type, self.data)


class LinearModel1(Model):
    def solve(self, criterion: Criterion, data, **kwargs):
        if criterion == Criterion.CRITERION_1:
            return lm.first.criterion_1.solve(data.c, data.A, data.b, Vars.M)
        elif criterion == Criterion.CRITERION_2:
            return lm.first.criterion_2.solve(data.c, data.A, data.b, Vars.z_min, Vars.alpha)
        elif criterion == Criterion.CRITERION_3:
            return lm.first.criterion_3.solve(data.c, data.A, data.b, Vars.weights)
        else:
            raise ValueError(f"Unsupported criterion for Linear Model 1: {type(criterion)}")


class LinearModel2(Model):
    def solve(self, criterion: Criterion, data, **kwargs):
        if criterion == Criterion.CRITERION_1:
            return lm.second.criterion_1.solve(data.c, data.A, data.b, data.d, Vars.M)
        elif criterion == Criterion.CRITERION_2:
            return lm.second.criterion_2.solve(data.c, data.A, data.b, data.d, Vars.z_min, Vars.alpha)
        elif criterion == Criterion.CRITERION_3:
            return lm.second.criterion_3.solve(data.c, data.A, data.b, data.d, Vars.weights)
        else:
            raise ValueError(f"Unsupported criterion for Linear Model 2: {str(criterion)}")


class LinearModel3(Model):
    def solve(self, criterion: Criterion, data, **kwargs):
        if criterion == Criterion.CRITERION_1:
            return lm.third.connected_model.solve(data.c, data.A, data.b, data.d, data.model_types, Vars.beta)
        else:
            raise ValueError(f"Unsupported criterion for Linear Model 3: {str(criterion)}")


class CombinatorialModel(Model):
    def solve(self, criterion: Criterion, data, **kwargs):
        if criterion == Criterion.CRITERION_1:
            return cm.first.criterion_1.solve(data.processing_times, data.precedence_graph, data.weights, Vars.M)
        elif criterion == Criterion.CRITERION_2:
            return cm.first.criterion_2.solve(data.processing_times, data.precedence_graph, data.weights,
                                              Vars.target_difference)
        else:
            raise ValueError(f"Unsupported criterion for Combinatorial Model: {str(criterion)}")
