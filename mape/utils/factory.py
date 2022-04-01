import datetime
from typing import Optional
import pathlib
import yaml

from logging import getLogger
from jsonschema import validate, ValidationError
from mape.monitoring import HybridMonitoring
from mape.analysis import HybridAnalysis
from mape.optimization import EconomicAdaptationProblemSolver
from mape.optimization.data import SolveArguments, ParetoFrontWeights, EconomicAdaptationParameters
from mape.planning import HybridPlanning
from mape.execution import ScalingExecution

BASE_PATH = pathlib.Path(__file__).parent.parent.resolve()

logger = getLogger()


class Factory:
    _config_schema: Optional[dict] = None

    def __init__(self, config: dict):
        """
        Args:
            config (dic): total config of the application
        Raises:
            ValidationError
        """
        self._config = config
        if Factory._config_schema is None:
            with open(BASE_PATH / 'config_schema.yaml', 'r') as schema_file:
                Factory._config_schema = yaml.load(schema_file, Loader=yaml.SafeLoader)
        try:
            validate(config, Factory._config_schema)
        except ValidationError as e:
            logger.error('config schema validation error.')
            raise e

    def get_hybrid_monitoring(self) -> HybridMonitoring:
        return HybridMonitoring(**self._config['monitoring'])

    def get_solve_arguments(self) -> SolveArguments:
        solve_config = self._config['optimization']['solve'].copy()
        solve_config['weights'] = ParetoFrontWeights(**solve_config['weights'])
        return SolveArguments(**solve_config)

    def get_problem_parameters(self) -> EconomicAdaptationParameters:
        return EconomicAdaptationParameters(**self._config['optimization']['problem'])

    def get_solver(self) -> EconomicAdaptationProblemSolver:
        return EconomicAdaptationProblemSolver(
            self.get_solve_arguments(),
            self.get_problem_parameters()
        )

    def get_hybrid_analysis(self) -> HybridAnalysis:
        return HybridAnalysis(self.get_solver(),
                              **self._config['analysis']['threshold'])

    def get_hybrid_planning(self) -> HybridPlanning:
        return HybridPlanning(**self._config['planning'])

    def get_scaling_execution(self) -> ScalingExecution:
        return ScalingExecution(**self._config['execution'])

    def get_mape_interval(self) -> datetime.timedelta:
        return datetime.timedelta(seconds=self._config['mape']['interval'])
