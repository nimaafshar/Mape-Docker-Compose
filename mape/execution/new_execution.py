import os
import sys
import subprocess


sys.path.insert(0, ".")

from execution.execution import Execution


class DockerExecution(Execution):
    def __init__(self, planning):
        super().__init__()
        super().set_planning(planning)

    def update(self):
        print("Execute\n")
        docker_compose_path = os.getcwd() + '/' + os.getenv("DOCKER_COMPOSE_FILE_DIRECTORY")
        print("docker compose path:",docker_compose_path)
        p = subprocess.Popen(["docker-compose", "-f",docker_compose_path, "up" ,"-d" ,"--scale", f"picalculator={self.planning.get_decision()}"],shell=True)
