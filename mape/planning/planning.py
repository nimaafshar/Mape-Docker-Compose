from abc import ABC, abstractmethod


class Planning(ABC):
    def __init__(self,mongodb_client):
        self.execution = None
        self.analysis = None
        self.mongodb_client = mongodb_client

    def database_insertion(self, data):
        self.mongodb_client["monitoring"]["planning"].insert_one(data)

    def set_analysis(self, analysis):
        self.analysis = analysis

    def attach(self, execution):
        self.execution = execution

    def detach(self):
        self.execution = None

    def notify(self):
        self.execution.update()

    @abstractmethod
    def update(self):
        pass
