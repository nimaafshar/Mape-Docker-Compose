from abc import ABC, abstractmethod
from typing import Optional

from ..cycle import CycleStep
from ..execution.data import ExecutionData
from .data import MonitoringData


class Monitoring(CycleStep, ABC):
    @abstractmethod
    def update(self, data: Optional[ExecutionData]) -> Optional[MonitoringData]:
        pass
