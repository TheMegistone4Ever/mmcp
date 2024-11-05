from mmcp.core import Model, ModelTypeError, CriterionError
from mmcp.utils import Vars, ModelType, Criterion
from .. import linear_models as lm, combinatorial_models as cm
from ..utils.logger_setup import LOGGER


class Solver:
    LOGGER.debug(f"Initialized {__name__}")

    def __init__(self, data, model_type: ModelType, criterion_type: Criterion):
        LOGGER.debug(f"Initializing Solver with data={data}, model_type={model_type}, criterion_type={criterion_type}")
        self.data = data
        self.model = self._create_model(model_type)
        self.criterion_type = criterion_type

    @staticmethod
    def _create_model(model_type: ModelType) -> Model:
        LOGGER.debug(f"Creating model of type: {model_type}")
        if model_type == ModelType.LINEAR_MODEL_1:
            return LinearModel1()
        elif model_type == ModelType.LINEAR_MODEL_2:
            return LinearModel2()
        elif model_type == ModelType.LINEAR_MODEL_3:
            return LinearModel3()
        elif model_type == ModelType.COMBINATORIAL_MODEL:
            return CombinatorialModel()
        else:
            LOGGER.error(f"Invalid model type: {model_type}")
            raise ModelTypeError(f"Invalid model type: {model_type}")

    def solve(self):
        LOGGER.debug(f"Solving model with criterion: {self.criterion_type}")
        return self.model.solve(self.criterion_type, self.data)

    def __str__(self):
        return f"\"{self.model}\" with criterion: \"{self.criterion_type}\""


class LinearModel1(Model):
    LOGGER.debug(f"Initialized {__name__}")

    def solve(self, criterion: Criterion, data, **kwargs):
        LOGGER.debug(f"Solving LinearModel1 with criterion: {criterion}")
        if criterion == Criterion.CRITERION_1:
            return lm.first.criterion_1.solve(data.c, data.A, data.b, Vars.M)
        elif criterion == Criterion.CRITERION_2:
            return lm.first.criterion_2.solve(data.c, data.A, data.b, Vars.z_min, Vars.alpha)
        elif criterion == Criterion.CRITERION_3:
            return lm.first.criterion_3.solve(data.c, data.A, data.b, Vars.weights)
        else:
            LOGGER.error(f"Unsupported criterion for Linear Model 1: {str(criterion)}")
            raise CriterionError(f"Unsupported criterion for Linear Model 1: {str(criterion)}")

    def __str__(self):
        return "Linear Model 1"


class LinearModel2(Model):
    LOGGER.debug(f"Initialized {__name__}")

    def solve(self, criterion: Criterion, data, **kwargs):
        LOGGER.debug(f"Solving LinearModel2 with criterion: {criterion}")
        if criterion == Criterion.CRITERION_1:
            return lm.second.criterion_1.solve(data.c, data.A, data.b, data.d, Vars.M)
        elif criterion == Criterion.CRITERION_2:
            return lm.second.criterion_2.solve(data.c, data.A, data.b, data.d, Vars.z_min, Vars.alpha)
        elif criterion == Criterion.CRITERION_3:
            return lm.second.criterion_3.solve(data.c, data.A, data.b, data.d, Vars.weights)
        else:
            LOGGER.error(f"Unsupported criterion for Linear Model 2: {str(criterion)}")
            raise CriterionError(f"Unsupported criterion for Linear Model 2: {str(criterion)}")

    def __str__(self):
        return "Linear Model 2"


class LinearModel3(Model):
    LOGGER.debug(f"Initialized {__name__}")

    def solve(self, criterion: Criterion, data, **kwargs):
        LOGGER.debug(f"Solving LinearModel3 with criterion: {criterion}")
        if criterion == Criterion.CRITERION_1:
            return lm.third.connected_model.solve(data.c, data.A, data.b, data.d, data.model_types, Vars.beta)
        else:
            LOGGER.error(f"Unsupported criterion for Linear Model 3: {str(criterion)}")
            raise CriterionError(f"Unsupported criterion for Linear Model 3: {str(criterion)}")

    def __str__(self):
        return "Linear Model 3 (Connected Model)"


class CombinatorialModel(Model):
    LOGGER.debug(f"Initialized {__name__}")

    def solve(self, criterion: Criterion, data, **kwargs):
        LOGGER.debug(f"Solving CombinatorialModel with criterion: {criterion}")
        if criterion == Criterion.CRITERION_1:
            return cm.first.criterion_1.solve(data.processing_times, data.precedence_graph, data.weights, Vars.M)
        elif criterion == Criterion.CRITERION_2:
            return cm.first.criterion_2.solve(data.processing_times, data.precedence_graph, data.weights,
                                              Vars.target_difference)
        else:
            LOGGER.error(f"Unsupported criterion for Combinatorial Model: {str(criterion)}")
            raise CriterionError(f"Unsupported criterion for Combinatorial Model: {str(criterion)}")

    def __str__(self):
        return "Combinatorial Model"
