from abc import ABC, abstractmethod
from typing import Optional, Dict, List
from logging import getLogger
import requests

from mape.cycle import CycleStep
from mape.execution.data import ExecutionData
from .data import MonitoringData

logger = getLogger()


class Monitoring(CycleStep, ABC):
    def __init__(self, interval: str):
        """
        Args:
            interval (str): monitoring interval in grafana timedelta format 1m,30s,....
        """
        self._interval: str = interval

    @abstractmethod
    def update(self, cycle: int, data: Optional[ExecutionData]) -> Optional[MonitoringData]:
        pass


class PrometheusMonitoring(Monitoring, ABC):
    def __init__(self, interval: str, host: str):
        """
        Args:
            interval (str): monitoring interval in grafana timedelta format 1m,30s,....
            host (str): prometheus host to query
        """
        super().__init__(interval)
        self._host = host

    def _query_instant_metric(self, querystring: str) -> Optional[str]:
        """
        Args:
            querystring (str): prometheus query
        Returns:
            None if it could not send query of results were unexpected
            otherwise prometheus result value
        """
        try:
            response = requests.get(self._host, {'query': querystring})
        except requests.exceptions.ConnectionError as e:
            logger.error(f"connection error while monitoring:{e}")
            return None
        if response.status_code >= 300 or response.status_code <= 200:
            logger.debug(
                f"invalid status code while monitoring:[code:{response.status_code},content:{response.content}]")
            return None
        content: Dict = response.json()
        if content.get('status') != 'success':
            logger.debug(
                f"querying was not successful:[content:{response.content}]")
            return None
        if content.get('data') is None:
            logger.debug(
                f"response doesn't contain key 'data':[content:{response.content}]")
            return None
        result = content.get('data').get('result', None)
        if result is None or len(result) == 0:
            logger.debug(
                f"response doesn't contain key ['data']['result'] or result doesn't have enough elements:"
                f"[content:{response.content}]")
            return None
        return result[0]['value'][1]
