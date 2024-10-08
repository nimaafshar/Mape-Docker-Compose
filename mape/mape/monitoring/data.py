import abc
from dataclasses import dataclass
from typing import Optional


@dataclass
class MonitoringData:
    """
    Base class for monitoring data type

    Args:
        cycle (int): cycle number we that data is generated in, starting from 0.
    """
    cycle: int

    def __post_init__(self) -> None:
        assert isinstance(self.cycle, int) and self.cycle >= 0, 'cycle is a non-negative integer'

    @property
    @abc.abstractmethod
    def is_complete(self) -> bool:
        """
        Returns:
            true if none of data fields is None,
            otherwise false
        """
        return self.cycle is not None


@dataclass
class SystemMonitoringData(MonitoringData):
    """
    System monitoring data type, used for monitoring hardware properties

    Args:
        cycle (int): cycle number we that data is generated in, starting from 0.
        cpu_utilization (float): used fraction of the cpu dedicated to monitored service between zero and 1
        memory_utilization (float): used fraction of the memory dedicated to monitored service between zero and 1
        number_of_containers (int): replicas of
    """
    cpu_utilization: Optional[float]
    memory_utilization: Optional[float]
    replicas: Optional[int]

    def __post_init__(self):
        super(SystemMonitoringData, self).__post_init__()
        if self.cpu_utilization is not None:
            assert 0 <= self.cpu_utilization <= 1, f'cpu utilization is a fraction. got {self.memory_utilization}'
        if self.memory_utilization is not None:
            assert 0 <= self.memory_utilization <= 1, f'memory utilization is a fraction. got {self.memory_utilization}'
        if self.replicas is not None:
            assert isinstance(self.replicas, int) > 0 and self.replicas > 0, 'replicas is a positive number'

    @property
    def is_complete(self) -> bool:
        return super(SystemMonitoringData, self).is_complete and \
               self.cpu_utilization is not None and \
               self.memory_utilization is not None and \
               self.replicas is not None


@dataclass
class APIMonitoringData(MonitoringData):
    """
    API monitoring data type, used for monitoring api response properties

    Args:
        cycle (int): cycle number we that data is generated in, starting from 0.
        avg_response_time (float): average response time of api in the last monitoring interval
        avg_data_length (float): average data length of requests to api in the last monitoring interval
        avg_rps (float): average number of requests per second sent to the api in the last monitoring interval
        sensor_count (int): last monitored count of sensors (users)
    """
    avg_response_time: Optional[float]
    avg_data_length: Optional[float]
    avg_rps: Optional[float]
    sensor_count: Optional[int]

    @property
    def is_complete(self) -> bool:
        return super(APIMonitoringData, self).is_complete and \
               self.avg_response_time is not None and \
               self.avg_data_length is not None and \
               self.avg_rps is not None and \
               self.sensor_count is not None


@dataclass
class HybridMonitoringData(MonitoringData):
    """
    we want both monitoring and system information, so we define a
    new data type that contains both
    Args:
        cycle (int): cycle number we that data is generated in, starting from 0.
        system (SystemMonitoringData): system monitoring data
        api (APIMonitoringData): api monitoring data
    """
    system: SystemMonitoringData
    api: APIMonitoringData

    @property
    def is_complete(self) -> bool:
        return super(HybridMonitoringData, self).is_complete and \
               self.system.is_complete and \
               self.api.is_complete
