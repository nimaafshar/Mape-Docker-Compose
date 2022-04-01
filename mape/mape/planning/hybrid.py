from typing import Optional
from logging import getLogger
from math import ceil

from .planning import Planning
from .data import PlanningData
from ..analysis.data import HybridAnalysisData, ThresholdAnalysisResult, EconomicAdaptationResults
from ..analysis.exceptions import DataInsufficiencyException

logger = getLogger()


class HybridPlanning(Planning):
    def __init__(self, min_replicas: int, max_replicas: int):
        """
        Args:
            min_replicas (int): minimum number of replicas for service, overrides scaling decisions
            max_replicas (int): maximum number of replicas for service, overrides scaling decisions
        """
        self._min_replicas: int = min_replicas
        self._max_replicas: int = max_replicas

    @staticmethod
    def _get_economic_scaling_decision(result: EconomicAdaptationResults) -> int:
        """
        get exact number of replicas from economic adaptation result.
        """
        return ceil(result.W)

    def _update(self, cycle: int, data: HybridAnalysisData) -> PlanningData:
        if not data.success:
            logger.info(f'analysis was not successful. taking no planning decision.[cycle:{cycle}]')
            return PlanningData(replicate=False, replicas=None)
        else:
            if data.threshold.result == ThresholdAnalysisResult.DO_NOT_SCALE:
                logger.info(f"threshold analysis didn't suggested scaling [cycle:{cycle}]")
                if data.economic.success:
                    economic_decision: int = self._get_economic_scaling_decision(data.economic.result)
                    logger.info(f"taking economic scaling decision. [cycle:{cycle}]")
                    return PlanningData(replicate=True, replicas=economic_decision)
                else:
                    logger.info(f"economic analysis was not successful. taking no planning decision.[cycle:{cycle}]")
                    return PlanningData(replicate=False, replicas=None)
            else:
                threshold_decision: int = data.threshold.replicas
                if data.economic.success:
                    economic_decision: int = self._get_economic_scaling_decision(data.economic.result)
                    if data.threshold.result == ThresholdAnalysisResult.SCALE_UP:
                        if economic_decision >= threshold_decision:
                            logger.info(
                                f"favourable suggestions. scale using economic suggestion. [cycle:{cycle}]")
                            return PlanningData(replicate=True, replicas=economic_decision)
                        else:
                            logger.info(
                                f"unfavourable suggestions. scale using threshold suggestion. [cycle:{cycle}]")
                            return PlanningData(replicate=True, replicas=threshold_decision)
                    elif data.threshold.result == ThresholdAnalysisResult.SCALE_DOWN:
                        if economic_decision <= threshold_decision:
                            logger.info(
                                f"favourable suggestions. scale using economic suggestion. [cycle:{cycle}]")
                            return PlanningData(replicate=True, replicas=economic_decision)
                        else:
                            logger.info(
                                f"unfavourable suggestions. scale using threshold suggestion. [cycle:{cycle}]")
                            return PlanningData(replicate=True, replicas=threshold_decision)
                else:
                    logger.info(
                        f"economic analysis was not successful. taking threshold planning decision.[cycle:{cycle},replicas:{threshold_decision}]")
                    return PlanningData(replicate=False, replicas=threshold_decision)

    def update(self, cycle: int, data: Optional[HybridAnalysisData]) -> PlanningData:
        if data is None:
            raise DataInsufficiencyException(data)
        planning_data: PlanningData = self._update(cycle, data)
        if planning_data.replicate:
            if planning_data.replicas > self._max_replicas:
                logger.info("replicas are more than maximum. overriding replicas.")
                planning_data.replicas = self._max_replicas
            elif planning_data.replicas < self._min_replicas:
                logger.info("replicas are less than maximum. overriding replicas.")
                planning_data.replicas = self._min_replicas
        return planning_data
