import os
import sys
import subprocess
import requests


sys.path.insert(0, ".")

from execution.execution import Execution


class DockerExecution(Execution):
    def __init__(self, threshold_planning, optimization_planning):
        super().__init__()
        super().set_threshold_planning(threshold_planning)
        super().set_optimization_planning(optimization_planning)

    def update(self):
        docker_compose_path = os.getcwd() + '/' + os.getenv("DOCKER_COMPOSE_FILE_DIRECTORY")
        #get status from threshold planning
        status = self.planning['threshold'].get_status()
        if not status:
            print("Status not found")
            return
        if status != 0:
            replicas = self.planning['threshold'].get_decision()
            print("applying threshold analysis decision")
        else:
            # get optimization planning decision
            replicas = self.planning['optimization'].get_decision()
            print("applying optimization analysis decision")
            
        if replicas is None:
            print("Replicas remain the same")
            return
        if replicas > 10:
            print("Replicas are going above maximum. going on with 10 replicas")
            repilcas = 10
        command = f"docker-compose -f {docker_compose_path} up -d --scale web={replicas} --no-recreate"
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
