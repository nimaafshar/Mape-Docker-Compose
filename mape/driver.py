import os
import time
from signal import signal, SIGINT
from sys import exit
import pymongo
import sys
import docker
from monitoring.new_monitoring import EASEMonitoring
from monitoring.docker_monitoring import DockerMonitoring
from analysis.new_analysis import EASEAnalysis
from analysis.docker_threshold_analysis import ThresholdAnalysis
from planning.new_planning import OptimizationPlanning
from mape.planning.threshold_planning import DockerPlanning
from execution.new_execution import DockerExecution
from dotenv import load_dotenv

load_dotenv()


def handler(signal_received, frame):
    exit(0)


def main():
    signal(SIGINT, handler)
    URI = os.getenv("URI")
    mongo_client = pymongo.MongoClient(URI)
    ease_monitoring = EASEMonitoring(mongo_client, docker.from_env())
    docker_monitoring = DockerMonitoring(mongo_client, docker.from_env())
    optimization_analysis = EASEAnalysis(mongo_client, ease_monitoring)
    threshold_analysis = ThresholdAnalysis(mongo_client,float(os.getenv("CPU_UPPER_THRESHOLD")),float(os.getenv("CPU_LOWER_THRESHOLD"))) 
    optimization_planning = OptimizationPlanning(optimization_analysis, mongo_client)
    docker_planning = DockerPlanning(mongo_client, threshold_analysis)

    execution = DockerExecution(docker_planning,optimization_planning,mongo_client,100)
    
    optimization_analysis.attach(optimization_planning)
    threshold_analysis.attach(docker_planning)
    docker_planning.attach(execution)
    optimization_planning.attach(execution)

    while True:
        docker_monitoring.get_measurements()
        ease_monitoring.get_measurements()
        threshold_analysis.update()
        optimization_analysis.update()
        time.sleep(EASEMonitoring.interval)


if __name__ == "__main__":
    main()
