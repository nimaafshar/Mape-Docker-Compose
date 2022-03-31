from typing import Optional
from logging import getLogger
import requests

from . import ExecutionData
from .execution import Execution
from ..planning import PlanningData

logger = getLogger()


class ScalingExecution(Execution):
    def __init__(self, scaling_endpoint: str):
        self._scaling_endpoint: str = scaling_endpoint

    def update(self, cycle: int, data: Optional[PlanningData]) -> Optional[ExecutionData]:
        if data is None:
            logger.info(f"no planning data. didn't take any action [cycle:{cycle}")
        else:
            if data.replicate:
                try:
                    response: requests.Response = requests.post(self._scaling_endpoint,
                                                                json={'replicas': data.replicas})
                    if response.status_code != 200:
                        logger.error(
                            f"error in scaling request: [cycle:{cycle},status:{response.status_code},content:{response.content}]")
                        return ExecutionData(success=False)
                    else:
                        return ExecutionData(success=True)
                except ConnectionError as e:
                    logger.error(f"connection error: {e}")
                    return ExecutionData(success=False)
            else:
                logger.info(f"no scaling action planned. didn't take any action [cycle:{cycle}")
        return ExecutionData(success=False)
