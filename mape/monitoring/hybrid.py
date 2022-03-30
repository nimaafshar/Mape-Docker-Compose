from typing import Optional

from .api import APIMonitoring
from .system import SystemMonitoring
from ..execution import ExecutionData
from .data import HybridMonitoringData, SystemMonitoringData, APIMonitoringData


class HybridMonitoring(SystemMonitoring, APIMonitoring):
    def __init__(self, interval: str, host: str, service_name: str):
        super().__init__(interval, host, service_name)

    def update(self, cycle: int, data: Optional[ExecutionData]) -> Optional[HybridMonitoringData]:
        sys_data: SystemMonitoringData = SystemMonitoring.update(self, cycle, data)
        api_data: APIMonitoringData = APIMonitoring.update(self, cycle, data)
        return HybridMonitoringData(
            cycle,
            sys_data.cpu_utilization,
            sys_data.memory_utilization,
            sys_data.replicas,
            api_data.avg_response_time,
            api_data.avg_data_length,
            api_data.avg_rps,
            api_data.sensor_count
        )
