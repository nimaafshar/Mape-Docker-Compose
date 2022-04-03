import pathlib
from typing import Optional
from logging import getLogger
import requests
import subprocess

from . import ExecutionData
from .execution import Execution
from ..planning import PlanningData

logger = getLogger()


class ScalingExecution(Execution):
    def __init__(self, service_name: str, compose_path: pathlib.Path):
        """
        Args:
            service_name(str): the service name you want to scale using docker-compose
            compose_path(pathlib.Path): docker compose file path
        """
        self._service_name: str = service_name
        self._compose_file_path: pathlib.Path = compose_path

    def update(self, cycle: int, data: Optional[PlanningData]) -> Optional[ExecutionData]:
        if data is None:
            logger.info(f"no planning data. didn't take any action [cycle:{cycle}")
        else:
            if data.replicate:
                result: subprocess.CompletedProcess = subprocess.run(
                    ['sudo', 'docker-compose', '-f', self._compose_file_path.absolute(), 'up', '--scale',
                     f'{self._service_name}={data.replicas}', ' -d'], capture_output=True)
                if result.returncode != 0:
                    logger.error(
                        f"error in scaling subprocess: [cycle:{cycle},stdout:{result.stdout},stderr:{result.stderr}]")
                    return ExecutionData(success=False)
                else:
                    return ExecutionData(success=True)
            else:
                logger.info(f"no scaling action planned. didn't take any action [cycle:{cycle}]")
        return ExecutionData(success=False)
