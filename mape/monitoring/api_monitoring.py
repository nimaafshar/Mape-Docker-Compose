from typing import Optional

from .data import APIMonitoringData
from .monitoring import PrometheusMonitoring
from ..execution import ExecutionData


class APIMonitoring(PrometheusMonitoring):

    def _query_avg_rps(self) -> Optional[float]:
        """
        average rps (requests per second) of the last monitoring interval
        returns None in case of connection problems or absence of data
        """
        query: str = f'rate(iotwg_web_response_time_count[{self._interval}])'
        result = self._query_instant_metric(query)
        return None if result is None else float(result)

    def _query_sensor_count(self) -> Optional[int]:
        """
        most recent sensor (user) count monitored.
        returns None in case of connection problems or absence of data
        """
        query: str = f'iotwg_sensor_count'
        result = self._query_instant_metric(query)
        return None if result is None else int(result)

    def _query_avg_response_time(self) -> Optional[float]:
        """
        average response time in the last monitoring interval in seconds.
        returns None in case of connection problems or absence of data
        """
        query: str = f'rate(iotwg_web_response_time_sum[{self._interval}])/' + \
                     f'rate(iotwg_web_response_time_count[{self._interval}])'
        result = self._query_instant_metric(query)
        return None if result is None else int(result)

    def _query_avg_request_length(self) -> Optional[float]:
        """
        average request data length in the last monitoring interval in bytes.
        returns None in case of connection problems or absence of data
        """
        query: str = f'rate(iotwg_web_request_length_sum[{self._interval}])/' + \
                     f'rate(iotwg_web_request_length_count[{self._interval}])'
        result = self._query_instant_metric(query)
        return None if result is None else float(result)

    def update(self, cycle: int, data: Optional[ExecutionData]) -> Optional[APIMonitoringData]:
        return APIMonitoringData(
            cycle,
            self._query_avg_response_time(),
            self._query_avg_request_length(),
            self._query_avg_rps(),
            self._query_sensor_count()
        )
