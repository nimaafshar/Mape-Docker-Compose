from typing import Optional

from .data import SystemMonitoringData
from .monitoring import PrometheusMonitoring
from ..execution import ExecutionData


class SystemMonitoring(PrometheusMonitoring):
    """
    query service metrics using cadvisor and prometheus
    """

    def __init__(self, interval: str, host: str, service_name: str):
        """
        Args:
            interval (str): monitoring interval in grafana timedelta format 1m,30s,....
            host (str): prometheus host to query
            service_name (str): the service which you want to monitor
        """
        super(SystemMonitoring, self).__init__(interval, host)
        self._service_name: str = service_name

    def _query_cpu_utilization(self) -> Optional[float]:
        """
        average cpu utilization of the last monitoring interval between 0 and 1
        returns None in case of connection problems or absence of data
        """
        query: str = 'sum(rate(container_cpu_usage_seconds_total' + \
                     '{container_label_com_docker_compose_service="' + self._service_name + '"}[' + self._interval \
                     + ']))/sum(container_spec_cpu_quota/' + \
                     'container_spec_cpu_period{container_label_com_docker_compose_service="' \
                     + self._service_name + '"})'

        result: Optional[str] = self._query_instant_metric(query)
        return result if result is None else float(result)

    def _query_memory_utilization(self) -> Optional[float]:
        """
        average memory utilization of the last monitoring interval between 0 and 1
        returns None in case of connection problems or absence of data
        """
        query: str = 'sum(container_memory_usage_bytes{container_label_com_docker_compose_service="' + self._service_name + \
                     '"}/ container_spec_memory_limit_bytes{container_label_com_docker_compose_service="' + self._service_name + \
                     '"})'
        result: Optional[str] = self._query_instant_metric(query)
        return result if result is None else float(result)

    def _query_replicas(self) -> Optional[int]:
        """
        number of containers for the target service
        returns None in case of connection problems or absence of data
        """
        query: str = 'count(container_last_seen{container_label_com_docker_compose_service="' + \
                     self._service_name + '"})'
        result: Optional[str] = self._query_instant_metric(query)
        return result if result is None else int(result)

    def update(self, cycle: int, data: Optional[ExecutionData]) -> Optional[SystemMonitoringData]:
        return SystemMonitoringData(cycle,
                                    self._query_cpu_utilization(),
                                    self._query_memory_utilization(),
                                    self._query_replicas())
