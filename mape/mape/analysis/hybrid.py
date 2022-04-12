from typing import Optional

from . import AnalysisData
from .threshold import ThresholdAnalysis
from .economic import EconomicAnalysis
from ..monitoring.data import HybridMonitoringData
from ..optimization import EconomicAdaptationProblemSolver
from .data import EconomicAnalysisData, ThresholdAnalysisData, HybridAnalysisData
from .exceptions import DataInsufficiencyException

from prometheus_client import Gauge, Enum
from logging import getLogger
from dataclasses import asdict

logger = getLogger()


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
        self._threshold_status: Enum = Enum('mape_threshold_analysis_status',
                                            'if threshold analysis was successful',
                                            states=('success', 'fail'))
        self._threshold_decision: Gauge = Gauge('mape_threshold_analysis_decision',
                                                'MAPE threshold analysis decision, scale up = +1,'
                                                'scale down = -1, do nothing = 0')
        self._threshold_replicas: Gauge = Gauge('mape_threshold_analysis_replicas',
                                                'MAPE threshold analysis suggested replicas.')

        self._economic_status: Enum = Enum('mape_economic_analysis_status',
                                           'if economic analysis was successful',
                                           states=('success', 'fail'))
        self._economic_service_price: Gauge = Gauge('mape_economic_analysis_service_price',
                                                    'MAPE Economic Analysis suggested p_s (service price)')
        self._economic_replicas: Gauge = Gauge('mape_economic_analysis_replicas',
                                               'MAPE Economic Analysis suggested W (replicas count)')
        self._ads_per_page: Gauge = Gauge('mape_economic_analysis_ads_count',
                                          'MAPE Economic Analysis suggested gamma (average banners per page)')
        self._service_profit: Gauge = Gauge('mape_economic_analysis_service_profit',
                                            'MAPE Economic Analysis optimized pi_s (service profit)')
        self._app_profit: Gauge = Gauge('mape_economic_analysis_app_profit',
                                        'MAPE Economic Analysis optimized pi_a (application profit)')
        self._user_satisfaction: Gauge = Gauge('mape_economic_analysis_user_satisfaction',
                                               'MAPE Economic Analysis optimized U (user satisfaction)')

    def update(self, cycle: int, data: Optional[HybridMonitoringData]) -> Optional[AnalysisData]:
        if data is None:
            raise DataInsufficiencyException(data)

        logger.debug(f"System Monitoring Data: {asdict(data.system)}")
        logger.debug(f"API Monitoring Data: {asdict(data.api)}")

        threshold_data: ThresholdAnalysisData = ThresholdAnalysis.update(self, cycle, data.system)
        economic_data: Optional[EconomicAnalysisData]
        try:
            economic_data = EconomicAnalysis.update(self, cycle, data.api)
        except DataInsufficiencyException:
            economic_data = EconomicAnalysisData(success=False, result=None)

        if threshold_data is not None and threshold_data.success:
            self._threshold_status.state('success')
            self._threshold_decision.set(int(threshold_data.result))
            self._threshold_replicas.set(threshold_data.replicas)
        else:
            self._threshold_status.state('fail')

        if economic_data is not None and economic_data.success:
            self._economic_status.state('success')
            self._economic_service_price.set(economic_data.result.p_s)
            self._economic_replicas.set(economic_data.result.W)
            self._ads_per_page.set(economic_data.result.gamma)
            self._service_profit.set(economic_data.result.pi_s)
            self._app_profit.set(economic_data.result.pi_a)
            self._user_satisfaction.set(economic_data.result.U)
        else:
            self._economic_status.state('fail')
        return HybridAnalysisData(success=threshold_data.success, economic=economic_data, threshold=threshold_data)
