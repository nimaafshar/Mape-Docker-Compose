from dataclasses import dataclass


@dataclass
class MonitoringData:
    """
    Base class for monitoring data type

    Args:
        cycle (int): cycle number we that data is generated in, starting from 0.
    """
    cycle: int

    def __post_init__(self):
        assert isinstance(self.cycle, int) and self.cycle >= 0, 'cycle is a non-negative integer'


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
    cpu_utilization: float
    memory_utilization: float
    replicas: int

    def __post_init__(self):
        super(SystemMonitoringData, self).__post_init__()
        assert 0 < self.cpu_utilization < 1, 'cpu utilization is a fraction'
        assert 0 < self.memory_utilization < 1, 'memory utilization is a fraction'
        assert isinstance(self.replicas, int) > 0 and self.replicas > 0, 'replicas is a positive number'


@dataclass
class APIMonitoringData(MonitoringData):
    """
    API monitoring data type, used for monitoring api response properties

    Args:
        cycle (int): cycle number we that data is generated in, starting from 0.
        avg_response_time (float): average response time of api in the last monitoring interval
        avg_data_length (float): average data length of requests to api in the last monitoring interval
        avg_rps (float): average number of requests per second sent to the api in the last monitoring interval
    """
    avg_response_time: float
    avg_data_length: float
    avg_rps: float


@dataclass
class CombinedMonitoringData(APIMonitoringData, SystemMonitoringData):
    """
    we want both monitoring and system information, so we define a
    new data type that contains both
    """
    pass
