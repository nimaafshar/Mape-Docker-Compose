from analysis.problem import solve_optimization_problem,AdaptationProblem
from planning.planning import Planning
from monitoring.new_monitoring import EASEMonitoring

class OptimizationPalnning(Planning):
    H = 10
    #in miliseconds
    response_time_upper_bound = 3000
    response_time_lower_bound = 1
    #in request per seconds
    container_capacity_lower_bound = 1
    container_capacity_upper_bound = 75
    #in dollars
    revenue_per_thousand_ads = 100
    #count
    banner_count_lower_bound = 1
    banner_count_upper_bound = 10
    #per kilobytes
    data_transfer_cost = 0.0001
    container_cost = 0.0002

    def __init__(self, analysis):
        # setting constants
        super().__init__()
        self.nb_containers = 0
        self.analysis = analysis

    def update(self):
        # last_data = super().get_last_data()
        # self.nb_containers = last_data.get("nb_containers")
        # total_net_usage = last_data.get('net_rx') + last_data.get('net_tx')
        problem = AdaptationProblem(
            landa=self.get_arrival_rate(),
            n=self.get_average_payload(),
            p_i=self.container_cost,
            p_n=self.data_transfer_cost,
            H=self.H,
            RPM=self.revenue_per_thousand_ads,
            R=self.get_response_time(),
            gamma_l=self.banner_count_lower_bound,
            gamma_u=self.banner_count_upper_bound,
            R_l=self.response_time_lower_bound,
            R_u=self.response_time_upper_bound,
            d_l=self.container_capacity_lower_bound,
            d_u=self.container_capacity_upper_bound
        )
        objectives, variables = solve_optimization_problem(problem)
        print("Analyse results:")
        print(f"p_s should be {variables[0]}")
        print(f"W should be {variables[1]}")
        print(f"gamma should be {variables[2]}")
        print("in optimal conditions:")
        print(f"service profit should be {objectives[0]}")
        print(f"client profit should be {objectives[1]}")
        print(f"user satisfaction should be {objectives[2]}")
        # we can also insert results into some sort of database
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
