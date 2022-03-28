from abc import abstractmethod, ABC
from typing import Optional

from ..cycle import CycleStep
from .data import ExecutionData
from ..planning.data import PlanningData


class Execution(CycleStep, ABC):
    @abstractmethod
    def update(self, data: Optional[PlanningData]) -> Optional[ExecutionData]:
        pass
