from typing import Optional
from logging import getLogger

from .analysis import Analysis
from .data import ThresholdAnalysisData, ThresholdAnalysisResult
from ..monitoring.data import SystemMonitoringData
from .exceptions import DataInsufficiencyException

logger = getLogger()


class ThresholdAnalysis(Analysis):
    def __init__(self, cpu_upper_threshold: float, cpu_lower_threshold: float):
        """
        Threshold analysis is based on cpu utilization only
        Args:
            cpu_lower_threshold (float): between 0 and 1, if less than this fraction of cpu is utilized
             , analysis result would be scale down
            cpu_upper_threshold (float): between 0 and 1, if more than this fraction of cpu is utilized
             , analysis result would be scale up
        """
        self._cpu_upper_threshold: float = cpu_upper_threshold
        self._cpu_lower_threshold: float = cpu_lower_threshold

    def update(self, cycle: int, data: Optional[SystemMonitoringData]) -> ThresholdAnalysisData:
        if not data.is_complete:
            raise DataInsufficiencyException(data)
        cpu_utilization: float = data.cpu_utilization
        result: ThresholdAnalysisResult
        if cpu_utilization < self._cpu_lower_threshold:
            result = ThresholdAnalysisResult.SCALE_DOWN
        elif cpu_utilization > self._cpu_upper_threshold:
            result = ThresholdAnalysisResult.SCALE_UP
        else:
            result = ThresholdAnalysisResult.DO_NOT_SCALE
        logger.info(f'threshold analysis successful. [cycle:{cycle},result:{result}]')
        return ThresholdAnalysisData(success=True, result=result, replicas=data.replicas + result)
