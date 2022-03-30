import abc
from typing import Any, Optional


class CycleStep(abc.ABC):

    @abc.abstractmethod
    def update(self, cycle: int, data: Optional) -> Any:
        """
        update this step using output of the previous step, and return output of this step
        any information about the state of step should be stored in objects memory, not input and output.
        """
        pass
