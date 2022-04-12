from dataclasses import dataclass
from typing import Optional


@dataclass
class PlanningData:
    """
    Args:
        replicate (bool): whether to change replicas of the service in execution
        replicas (int): number of replicas for service, if replicate is true
    """
    replicate: bool
    replicas: Optional[int]

    def __post_init__(self):
        assert isinstance(self.replicate, bool)
        assert not self.replicate or (isinstance(self.replicas, int) and self.replicas >= 0)
