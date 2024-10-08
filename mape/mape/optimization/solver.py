import numpy
import numpy as np

from .data import SolveArguments, EconomicAdaptationParameters, EconomicAdaptationResults
from .optimization import EconomicAdaptationProblem

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.util.termination.max_gen import MaximumGenerationTermination
from pymoo.optimize import minimize
from pymoo.core.result import Result
from pymoo.factory import get_termination

from typing import Tuple, Optional
from logging import getLogger

logger = getLogger()


class EconomicAdaptationProblemSolver:
    def __init__(self, solve_arguments: SolveArguments, problem_params: EconomicAdaptationParameters):
        self._args: SolveArguments = solve_arguments
        self._problem_params: EconomicAdaptationParameters = problem_params
        self._algorithm: NSGA2 = NSGA2(pop_size=solve_arguments.pop_size, n_offsprings=solve_arguments.n_offsprings,
                                       eliminate_duplicates=solve_arguments.eliminate_duplicates)
        self._termination: MaximumGenerationTermination = get_termination('n_gen',
                                                                          solve_arguments.termination_generation)

    def _optimize(self, problem: EconomicAdaptationProblem) -> Optional[Tuple[numpy.ndarray, numpy.ndarray]]:
        """
        optimizing the problem using NSGA2 algorithm and max_gen termination.
        Args:
            problem (EconomicAdaptationProblem): pymoo problem
        Returns:
            (None,None) if optimization has no result,
            otherwise (objectives, variables)
        """
        res: Result = minimize(problem=problem,
                               algorithm=self._algorithm,
                               termination=self._termination,
                               save_history=True,
                               verbose=False
                               )
        # you can find objectives in res.F and variables in res.X
        return res.F, res.X

    def _choose_on_pareto_front(self, pareto_f: np.ndarray, design_space: np.ndarray) -> Tuple[float, float, float]:
        """
        choose one point in pareto front (set of optimization result)
        Args:
            pareto_f (numpy.ndarray): pareto front set (-1 * objectives set)
            design_space (numpy.ndarray): design space (variables set)
        Returns:
            (p_s,W,gamma)
        """
        max_values: np.ndarray = np.max(pareto_f, axis=0)
        # only purpose of p1,p2,p3 is code formatting
        p1: np.ndarray = pareto_f[:, 0] * self._args.weights.service / max_values[0]
        p2: np.ndarray = pareto_f[:, 1] * self._args.weights.application / max_values[1]
        p3: np.ndarray = pareto_f[:, 2] * self._args.weights.user / max_values[2]
        arg_max = np.argmax(p1 + p2 + p3)
        return tuple(design_space[arg_max])

    def solve(self, _lambda: float, n: float, r: float) -> Optional[EconomicAdaptationResults]:
        """
        Args:
            _lambda (float): arrival rate (req/s)
            n (float): average data payload for each request (KB)
            r (float): response time (ms)
        Returns:
            None if maximum number of tries doesn't produce result
            otherwise, optimization results (EconomicAdaptationResults)
        """
        objectives: Optional[numpy.ndarray] = None
        variables: Optional[numpy.ndarray] = None
        for i in range(self._args.max_tries):
            problem: EconomicAdaptationProblem = EconomicAdaptationProblem(self._problem_params, _lambda, n, r)
            objectives, variables = self._optimize(problem)
            if objectives is not None and variables is not None:
                logger.debug(f'optimization problem solved in try:{i}')
                break

        if objectives is None or variables is None:
            logger.debug(f"couldn't find any solution. in {self._args.max_tries} tries.")
            # optimization failed
            return None
        else:
            # optimization succeeded
            p_s: float
            W: float
            gamma: float
            p_s, W, gamma = self._choose_on_pareto_front(-1 * objectives, variables)

            pi_s: float = (p_s * _lambda) - (self._problem_params.p_i * W) - (n * self._problem_params.p_n * _lambda)
            pi_a: float = (gamma * self._problem_params.RPM / 1000 * _lambda) - (self._problem_params.H * _lambda) - \
                          (p_s * _lambda)
            U: float = (self._problem_params.a * (self._problem_params.gamma_u - gamma) /
                        (self._problem_params.gamma_u - self._problem_params.gamma_l)) + \
                       (self._problem_params.b * (self._problem_params.R_u - r) / (
                               self._problem_params.R_u - self._problem_params.R_l))
            return EconomicAdaptationResults(p_s, W, gamma, pi_s, pi_a, U)
