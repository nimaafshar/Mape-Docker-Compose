from monitoring.monitoring import Monitoring
import subprocess
import random
import datetime
import os
import sys
import time

import docker
import pymongo
import pytz
from signal import signal, SIGINT
from sys import exit


class EASEMonitoring(Monitoring):
    interval = 60  # monitoring interval in seconds
    cycle_number = 0
    raw_results = None
    successful = False

    def __init__(self, mongodb_client, env_client):
        self.host = os.getenv("BACKEND_HOST")
        self.port = os.getenv("BACKEND_PORT")
        # reading request property set
        self.request_property_set = []
        with open("mape/request_property_set.txt", 'r') as f:
            for line in f:
                splited = line.split()
                if len(splited) < 2:
                    raise Exception("Invalid request_property_set.txt format there should be 2 integers in a line")
                try:
                    requests, concurrent_users = int(splited[0]), int(splited[1])
                    self.request_property_set.append((requests,concurrent_users))
                except Exception as e:
                    raise Exception("invalid request_property_set.txt format it should contain integers")

        super().__init__(mongodb_client, env_client)

    def get_digits_count(self):
        return random.randint(5, 800)

    def get_request_properties(self):
        """
        returns a pair consisting of request_count and concurent_users_count
        """
        #                                      |-> traffic uprising
        # request_property_set = [(100, 20), (20, 5), (1000, 100), (400, 50), (300, 30), (160, 20), (100, 10)]

        return self.request_property_set[self.cycle_number % len(self.request_property_set)]

    def get_measurements(self):
        self.cycle_number += 1
        # this part uses apache benchmark to send requests to server
        digits = self.get_digits_count()
        request_number, concurent_users = self.get_request_properties()
        url = "http://" + self.host + ":" + self.port + "/?d=" + str(digits)
        print("sending " + str(request_number) + " requests by " + str(concurent_users) + " concurrent users")
        # using an apache benchmark subprocess to
        print("running this command:",['ab', '-n', str(request_number), '-c', str(concurent_users), url])
        result = subprocess.run(['ab', '-n', str(request_number), '-c', str(concurent_users), url],
                                stdout=subprocess.PIPE)
        self.raw_results = result.stdout.decode('utf-8')
        if "Connection refused" in self.raw_results:
            # failed to fetch results restart the backend-docker-container
            print("CONNECTION REFUSED")
        elif "Server Software" in self.raw_results:
            # results fetch was successful
            # -printing results to a file
            filename = "log/ab-output-" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(filename, 'w') as f:
                f.write(self.raw_results)
            self.successful = True
        else:
            print("ANOTHER ERROR happened:")
            print(self.raw_results)
        pass


def handler(signal_received, frame):
    exit(0)

# def main():
#     signal(SIGINT, handler)
#     monitoring = EASEMonitoring(pymongo.MongoClient(os.getenv("URI")), docker.from_env())
#     while True:
#         monitoring.get_measurements()
#         time.sleep(DockerMonitoring.interval)
#
#
# if __name__ == "__main__":
#     main()
