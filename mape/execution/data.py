from dataclasses import dataclass


@dataclass
class ExecutionData:
    """
    Args:
        success (bool): if scaling was successful.
    """
    success: bool
