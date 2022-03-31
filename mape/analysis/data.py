from dataclasses import dataclass
from ..optimization.data import EconomicAdaptationResults

from typing import Optional
from enum import IntEnum


class ThresholdAnalysisResult(IntEnum):
    SCALE_UP = 1
    SCALE_DOWN = -1
    DO_NOT_SCALE = 0


@dataclass
class AnalysisData:
    """
    Args:
        success (bool): if analysis was successful
    """
    success: bool


@dataclass
class ThresholdAnalysisData(AnalysisData):
    """
    Args:
        success (bool): if analysis was successful
        result (ThresholdAnalysisDecision): analysis result which suggests you have to scale up,down or do nothing
        replicas (int): suggested number of replicas, non-negative
    """
    result: ThresholdAnalysisResult
    replicas: int

    def __post_init__(self):
        assert isinstance(self.result, ThresholdAnalysisResult)
        assert isinstance(self.replicas, int) and self.replicas >= 0


@dataclass
class EconomicAnalysisData(AnalysisData):
    """
    Args:
        success (bool): if analysis was successful
        result (EconomicAdaptationResults): analysis result which suggests service price,
         service replicas and number of banners per page
    """
    result: Optional[EconomicAdaptationResults]


@dataclass
class HybridAnalysisData(AnalysisData):
    """
    Args:
        success (bool): if analysis was successful
        economic (EconomicAnalysisData): data from economic analysis
        threshold (ThresholdAnalysisData): data from threshold analysis
    """
    economic: EconomicAnalysisData
    threshold: ThresholdAnalysisData
