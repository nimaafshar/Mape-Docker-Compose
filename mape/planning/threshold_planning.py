import sys

sys.path.insert(0, ".")

from planning.planning import Planning


class DockerPlanning(Planning):
    def __init__(self, mongodb_client, analysis):
        super().__init__(mongodb_client)
        super().set_analysis(analysis)
        self.decision = None
        self.status = None
        # self.nb_containers = 0

    def get_decision(self):
        return self.decision
    
    def get_status(self):
        return self.status

    def update(self):
        # self.nb_containers = self.analysis.get_nb_containers()
        self.decision = self.analysis.nb_containers + self.analysis.get_result()
        self.status = self.analysis.get_status()
        if self.decision < 1:
            self.decision = 1
        print("Plan\n")
        self.notify()
