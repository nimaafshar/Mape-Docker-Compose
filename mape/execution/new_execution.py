import os
import sys
import subprocess
import requests


sys.path.insert(0, ".")

from execution.execution import Execution


class DockerExecution(Execution):
    def __init__(self, planning):
        super().__init__()
        super().set_planning(planning)

    def update(self):
        docker_compose_path = os.getcwd() + '/' + os.getenv("DOCKER_COMPOSE_FILE_DIRECTORY")
        repilcas = self.planning.get_decision()
        if repilcas is None:
            print("Replicas remain the same")
            return
        if repilcas > 10:
            repilcas = 10
        command = f"docker-compose -f {docker_compose_path} up -d --scale picalculator={replicas} --no-recreate"
        print("Execute:",command)
    
        # response = requests.get(url)
        # print("DOCKER MANAGER RESULTS:",response.text)
        
        # p = subprocess.Popen(["docker-compose", "-f",docker_compose_path, "up" ,"-d" ,"--scale", f"picalculator={self.planning.get_decision()}"],shell=True)
        p = subprocess.Popen(command,
                            shell=True,
                            stdout=subprocess.PIPE,
                            close_fds=True,
                            stderr=subprocess.STDOUT)
        print("results:",p.stdout.read().decode('utf-8'))
