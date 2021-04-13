from abc import abstractmethod, ABC


class Execution(ABC):
    def __init__(self,mongodb_client):
        self.planning = {
            "optimization": None,
            "threshold" : None
        }
        self.mongodb_client = mongodb_client
        

    def set_threshold_planning(self, planning):
        self.planning['threshold'] = planning
    
    def set_optimization_planning(self,planning):
        self.planning['optimization'] = planning
    
    def database_insertion(self, data):
        self.mongodb_client["monitoring"]["execution"].insert_one(data)

    @abstractmethod
    def update(self):
        pass
