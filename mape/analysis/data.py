from dataclasses import dataclass
from ..optimization.data import EconomicAdaptationResults

from enum import Enum


class ThresholdAnalysisResult(Enum):
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
        result (ThresholdAnalysisDecision): analysis result which suggests you have to scale up,down or do nothing
    """
    result: ThresholdAnalysisResult


@dataclass
class EconomicAnalysisData(AnalysisData):
    """
    Args:
        result (EconomicAdaptationResults): analysis result which suggests service price,
         service replicas and number of banners per page
    """
    result: EconomicAdaptationResults
