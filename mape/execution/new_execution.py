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
        docker_compose_path = os.getcwd() + '/' + os.getenv("DOCKER_COMPOSE_FILE_DIRECTORY")
        print("Execute:",f"docker-compose -f {docker_compose_path} up -d --scale picalculator={self.planning.get_decision()}")
        # p = subprocess.Popen(["docker-compose", "-f",docker_compose_path, "up" ,"-d" ,"--scale", f"picalculator={self.planning.get_decision()}"],shell=True)
        p = subprocess.Popen(f"docker-compose -f {docker_compose_path} up -d --scale picalculator={self.planning.get_decision()}",shell=True)
