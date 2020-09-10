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
        with open(os.getenv("DOCKER_COMPOSE_FILE_DIRECTORY"),'r') as f:
            print("docker compose:",f.readline())
        os.system("sudo docker-compose -f {} up -d --scale picalculator={}".format(os.getenv("DOCKER_COMPOSE_FILE_DIRECTORY"),
                                                                     self.planning.get_decision()))
