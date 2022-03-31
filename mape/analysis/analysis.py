from abc import ABC, abstractmethod
from typing import Optional

from ..cycle import CycleStep
from ..monitoring.data import MonitoringData
from .data import AnalysisData


class Analysis(CycleStep, ABC):
    @abstractmethod
    def update(self, cycle: int, data: Optional[MonitoringData]) -> Optional[AnalysisData]:
        pass
