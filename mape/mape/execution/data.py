from dataclasses import dataclass


@dataclass
class ExecutionData:
    """
    Args:
        success (bool): if execution was successful.
    """
    success: bool
