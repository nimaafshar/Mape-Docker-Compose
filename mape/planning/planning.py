from abc import ABC, abstractmethod
from typing import Optional

from ..cycle import CycleStep
from ..analysis.data import AnalysisData
from .data import PlanningData


class Planning(CycleStep, ABC):
    @abstractmethod
    def update(self, cycle: int, data: Optional[AnalysisData]) -> Optional[PlanningData]:
        pass
