from analysis.problem import solve_optimization_problem, AdaptationProblem, choose_on_pf
from planning.planning import Planning
from analysis.new_analysis import EASEAnalysis
from monitoring.new_monitoring import EASEMonitoring
import os
from datetime import datetime


class OptimizationPlanning(Planning):
    H = 10
    # in miliseconds
    response_time_upper_bound = os.environ.get("RESPONSE_TIME_UPPER_BOUND", 2500)
    response_time_lower_bound = os.environ.get("RESPONSE_TIME_LOWER_BOUND", 10)
    # in request per seconds
    container_capacity_lower_bound = os.environ.get("CONTAINER_CAP_LOWER_BOUND", 10)
    container_capacity_upper_bound = os.environ.get("CONTAINER_CAP_UPPER_BOUND", 200)
    # count
    banner_count_lower_bound = os.environ.get("BANNER_LOWER_BOUND", 1)
    banner_count_upper_bound = os.environ.get("BANNER_UPPER_BOUND", 10)

    def __init__(self, analysis: EASEAnalysis, mongodb_client):
        # setting constants
        super().__init__(mongodb_client)
        self.nb_containers = 0
        self.analysis = analysis
        self.mongodb_client = mongodb_client

    def update(self):
        # last_data = super().get_last_data()
        # self.nb_containers = last_data.get("nb_containers")
        # total_net_usage = last_data.get('net_rx') + last_data.get('net_tx')
        objectives, variables = None,None
        for i in range(10):
            print("trying to solve optimiation problem: try"+str(i+1))
            problem = AdaptationProblem(
                landa=self.get_arrival_rate(),
                n=self.get_average_payload(),  # you can change KB to bytes
                R=self.get_response_time(),
                gamma_l=self.banner_count_lower_bound,
                gamma_u=self.banner_count_upper_bound,
                R_l=self.response_time_lower_bound,
                R_u=self.response_time_upper_bound,
                d_l=self.container_capacity_lower_bound,
                d_u=self.container_capacity_upper_bound
            )
            objectives, variables = solve_optimization_problem(problem)
            if objectives is not None and variables is not None:
                break
        
        print("Analyse results:")
        if objectives is None or variables is None:
            print("no optimized answer found for the problem")
            p_s = None
            W = None
            gamma = None
        else:
            p_s, W, gamma = choose_on_pf(-1 * objectives, variables)
            print("Optimized Results:")
            print({
                "p_s": p_s,
                "W": W,
                "gamma": gamma
            })
        # we can also insert results into some sort of database
        requests , con_users = self.analysis.monitoring.get_request_properties()
        data = {
            "requests":requests,
            "concurrent_users":con_users,
            "arrival_rate": self.analysis.arrival_rate,
            "response_time": self.analysis.response_time,
            "data_payload": self.analysis.data_payload,
            "predicted_p_s": p_s,
            "predicted_W": W,
            "predicted_gamma": gamma,
            "date": datetime.now()
        }
        super().database_insertion(data)

        # if you want to use execution step uncomment line below
        # super().notify()

    def get_arrival_rate(self):
        if self.analysis.arrival_rate is None:
            raise Exception("arrival rate is None")
        else:
            return self.analysis.arrival_rate

    def get_response_time(self):
        if self.analysis.response_time is None:
            raise Exception("response time is None")
        else:
            return self.analysis.response_time

    def get_average_payload(self):
        if self.analysis.data_payload is None:
            raise Exception("data payload is None")
        else:
            return self.analysis.data_payload

    def get_monitoring_time(self):
        return EASEMonitoring.interval  # in seconds
