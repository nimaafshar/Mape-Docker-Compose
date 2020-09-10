import os
import time
from signal import signal, SIGINT
from sys import exit
import pymongo
import sys
import docker
from monitoring.new_monitoring import EASEMonitoring
from analysis.new_analysis import EASEAnalysis
from planning.new_planning import OptimizationPlanning
from execution.new_execution import DockerExecution


# from execution.docker_execution import DockerExecution
# from planning.threshold_planning import DockerPlanning


def handler(signal_received, frame):
    exit(0)


def main():
    signal(SIGINT, handler)
    URI = os.getenv("URI")
    mongo_client = pymongo.MongoClient(URI)
    monitoring = EASEMonitoring(mongo_client, docker.from_env())
    analysis = EASEAnalysis(mongo_client, monitoring)
    planning = OptimizationPlanning(analysis, mongo_client)
    execution = DockerExecution(planning)
    
    analysis.attach(planning)
    planning.attach(execution)

    while True:
        monitoring.get_measurements()
        analysis.update()
        time.sleep(EASEMonitoring.interval)


if __name__ == "__main__":
    main()
