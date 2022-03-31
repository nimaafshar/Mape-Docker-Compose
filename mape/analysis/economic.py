from logging import getLogger
from typing import Optional

from .data import EconomicAnalysisData
from .analysis import Analysis
from .exceptions import DataInsufficiencyException
from ..monitoring.data import APIMonitoringData
from ..optimization import EconomicAdaptationProblemSolver, EconomicAdaptationResults

logger = getLogger()


class EconomicAnalysis(Analysis):
    def __init__(self, solver: EconomicAdaptationProblemSolver):
        """
        Args:
            solver (EconomicAdaptationProblemSolver): used to solve the optimization many times
        """
        self._solver = solver

    def update(self, cycle: int, data: Optional[APIMonitoringData]) -> EconomicAnalysisData:
        if not data.is_complete:
            raise DataInsufficiencyException(data)
        result: Optional[EconomicAdaptationResults] = self._solver.solve(data.avg_rps, data.avg_data_length,
                                                                         data.avg_response_time)
        if result is None:
            logger.error(f'economic analysis unsuccessful. [cycle:{cycle}]')
            return EconomicAnalysisData(success=False, result=None)
        else:
            logger.info(f'economic analysis successful. [cycle:{cycle},service_price:{result.p_s},replicas:{result.W}'
                        f',ads:{result.gamma}]')
            return EconomicAnalysisData(success=True, result=result)
