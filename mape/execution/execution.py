from abc import abstractmethod, ABC


class Execution(ABC):
    def __init__(self):
        self.planning = {
            "optimization": None,
            "threshold" : None
        }

    def set_threshold_planning(self, planning):
        self.planning['threshold'] = planning
    
    def set_optimization_planning(self,planning):
        self.planning['optimization'] = planning

    @abstractmethod
    def update(self):
        pass
