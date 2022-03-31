from dataclasses import dataclass


@dataclass
class ParetoFrontWeights:
    """
    Args:
        application (float): weight of the application in pareto front choosing strategy
        service (float): weight of the service in pareto front choosing strategy
        user (float): weight of the user in pareto front choosing strategy
    """
    application: float
    service: float
    user: float


@dataclass
class EconomicAdaptationResults:
    """
    Args:
        p_s (float): price per request in request/dollar
        W (float): number of service (backend) replicas
        gamma (float): average number of ad banners per page
    """
    p_s: float
    W: float
    gamma: float


@dataclass
class SolveArguments:
    """
    Args:
        pop_size
    """
    pop_size: int
    n_offsprings: int
    termination_generation: int
    max_tries: int
    weights: ParetoFrontWeights
    eliminate_duplicates: bool = True


@dataclass
class EconomicAdaptationParameters:
    """
    parameters of the economic adaptation problem that are constant throughout the program
    Args:
        p_i (float): cost of a virtual machine in dollars per second, positive
        p_n (float): cost of data transfer in dollars per KB, positive
        H (float): static hosting cost in dollars per second
        RPM (float): revenue per 1000 ads in dollars
        gamma_l (float): lower bound for average number of ads per page
        gamma_u (float): upper bound for average number of ads per page
        R_l (int): response time lower bound (milliseconds) for single VM
        R_u (int): response time upper bound (milliseconds) for single VM
        d_l (int): lower bound for capacity of each VM (requests/s)
        d_u (int): upper bound for capacity of each VM (requests/s)
    """
    p_i: float
    p_n: float
    H: float
    RPM: float
    gamma_l: int
    gamma_u: int
    R_l: int
    R_u: int
    d_l: int
    d_u: int
