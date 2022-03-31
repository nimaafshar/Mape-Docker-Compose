from typing import Optional

from . import AnalysisData
from .threshold import ThresholdAnalysis
from .economic import EconomicAnalysis
from ..monitoring.data import HybridMonitoringData
from ..optimization import EconomicAdaptationProblemSolver
from .data import EconomicAnalysisData, ThresholdAnalysisData, HybridAnalysisData
from .exceptions import DataInsufficiencyException


class HybridAnalysis(EconomicAnalysis, ThresholdAnalysis):
    def __init__(self, solver: EconomicAdaptationProblemSolver, cpu_upper_threshold: float, cpu_lower_threshold: float):
        """
        Args:
            solver (EconomicAdaptationProblemSolver): used to solve the optimization
            cpu_lower_threshold (float): between 0 and 1, if less than this fraction of cpu is utilized
             , analysis result would be scale down
            cpu_upper_threshold (float): between 0 and 1, if more than this fraction of cpu is utilized
             , analysis result would be scale up
        """
        EconomicAnalysis.__init__(self, solver)
        ThresholdAnalysis.__init__(self, cpu_upper_threshold, cpu_lower_threshold)

    def update(self, cycle: int, data: Optional[HybridMonitoringData]) -> Optional[AnalysisData]:
        if data is None:
            raise DataInsufficiencyException(data)
        threshold_data: ThresholdAnalysisData = ThresholdAnalysis.update(self, cycle, data.system)
        economic_data: EconomicAnalysisData = EconomicAnalysis.update(self, cycle, data.api)
        return HybridAnalysisData(success=threshold_data.success, economic=economic_data, threshold=threshold_data)
