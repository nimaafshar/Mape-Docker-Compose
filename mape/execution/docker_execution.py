import os
import sys


sys.path.insert(0, ".")

from execution.execution import Execution


class DockerExecution(Execution):
    def __init__(self, planning):
        super().__init__()
        super().set_planning(planning)

    def update(self):
        print("Execute\n")
        print(os.getenv("DOCKER_COMPOSE_FILE_DIRECTORY"))
        os.system("docker-compose -f {} up -d --scale web={}".format(os.getenv("DOCKER_COMPOSE_FILE_DIRECTORY"),
                                                                     self.planning.get_decision()))
