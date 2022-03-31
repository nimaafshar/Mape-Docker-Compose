from typing import Optional

from . import ExecutionData
from .execution import Execution
from ..planning import PlanningData


class ScalingExecution(Execution):
    def update(self, cycle: int, data: Optional[PlanningData]) -> Optional[ExecutionData]:
        # todo: change replicas in docker compose
        pass
