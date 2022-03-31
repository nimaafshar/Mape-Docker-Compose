import numpy as np
from pymoo.core.problem import Problem
from .data import EconomicAdaptationParameters


class EconomicAdaptationProblem(Problem):

    def __init__(self, params: EconomicAdaptationParameters, _lambda: float, n: float, r: float):
        """
        Args:
            params (EconomicAdaptationParameters): constant parameters in all
            _lambda (float): arrival rate (req/s)
            n (float): average data payload for each request (KB)
            r (float): response time (ms)
        """
        self._params: EconomicAdaptationParameters = params
        self._lambda: float = _lambda
        self._n: float = n
        self._r: float = r
        # weights in user satisfaction formula todo: investigate more in paper
        self._a = 0.5
        self._b = 0.5
        # p_s doesn't have any bound, so we should feed algorithm
        # a very high number for upper bound and 0 for lower bound
        super().__init__(n_var=3,  # p_s,W,gamma
                         n_obj=3,  # pi_s,pi_a,U
                         n_constr=4,
                         #            | investigate this
                         xl=np.array([0, _lambda / self._params.d_u, self._params.gamma_l]),
                         xu=np.array([10000, _lambda / self._params.d_l, self._params.gamma_u]))

    def _evaluate(self, x, out, *args, **kwargs):
        # objectives
        # to maximize objectives we multipy them by -1 and then minimize them
        # objectives are not normalized. todo: test normalization on results
        d = self._lambda / x[:, 1]
        rel_d = (d - self._params.d_l) / (self._params.d_u - self._params.d_l)
        R = ((self._params.R_u - self._params.R_l) * rel_d) + self._params.R_l
        pi_s = x[:, 0] * self._lambda - self._params.p_i * x[:, 1] - self._n * self._params.p_n * self._lambda
        pi_a = (x[:, 2] * self._params.RPM / 1000) * self._lambda - self._params.H * self._lambda - x[:,
                                                                                                    0] * self._lambda
        U = self._a * ((self._params.gamma_u - x[:, 2]) / (self._params.gamma_u - self._params.gamma_l)) + self._b * (
                (self._params.R_u - R) / (self._params.R_u - self._params.R_l))

        out["F"] = np.column_stack([-1 * pi_s, -1 * pi_a, -1 * U])

        # constrains (equations are flipped in a way that they would be less than zero)
        g1 = x[:, 0] - (x[:, 2] * self._params.RPM / 1000)
        g2 = -1 * pi_s
        g3 = -1 * pi_a
        g4 = (0.8 - U)

        out["G"] = np.column_stack([g1, g2, g3, g4])
