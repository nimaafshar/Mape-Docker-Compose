import numpy as np
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_problem, get_termination
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
from pymoo.model.problem import Problem


class AdaptationProblem(Problem):
    """
    response times are filled based on papers values(page8-table1)
    """
    def __init__(self,
                landa=50, #arrival rate (req/s)
                n=10, #average data payload for each request (KB)
                p_i=2.64E-04, #cost of a VM ($/s)
                p_n=3.50E-06, #cost of data transfer ($/KB)
                H=8.50E-05, #static Hosting cost ($/s)
                RPM=0.7, #revenue per 1000 ads ($)
                R=100, #response time (ms)
                gamma_l=1, #gamma lower bound (gamma is average number of ad banners per page)
                gamma_u=10, #gamma upper bound
                R_l=45, # respose time lower bound
                R_u=200, # response time upper bound
                d_l=15, #capacity of each VM lower bound(request/s)
                d_u=21 #capacity of each VM upper bound(request/s)
                ): 
        self.landa = landa
        self.n = n
        self.p_i = p_i
        self.p_n = p_n
        self.H = H
        self.RPM = RPM
        self.R = R
        self.gamma_l = gamma_l
        self.gamma_u = gamma_u
        self.R_l = R_l
        self.R_u = R_u
        self.d_l = d_l
        self.d_u = d_u
        #weights in user satisfaction formula
        self.a = 0.5
        self.b = 0.5
        #p_s doesn't have any bound so we should feed algorithm 
        #a very high number for upper bound and 0 (logically) for lower bound
        super().__init__(n_var=3, #p_s,W,gamma
                         n_obj=3, #pi_s,pi_a,U
                         n_constr=4,
                         xl=np.array([0,landa/d_u,gamma_l]),
                         xu=np.array([10000,landa/d_l,gamma_u]))

    def _evaluate(self, x, out, *args, **kwargs):
        #objectives
        #to maximize objectives we multipy them by -1 and then minimize them 
        #objectives are not normalized. test normalization on results
        d = self.landa/x[:,1]
        rel_d = (d - self.d_l) / (self.d_u - self.d_l)
        R = ((self.R_u-self.R_l)*rel_d) + self.R_l
        pi_s = x[:,0]*self.landa - self.p_i*x[:,1] - self.n*self.p_n*self.landa
        pi_a = (x[:,2]*self.RPM/1000)*self.landa - self.H*self.landa - x[:,0]*self.landa
        U = self.a*((self.gamma_u-x[:,2])/(self.gamma_u-self.gamma_l)) + self.b*((self.R_u-R)/(self.R_u-self.R_l))
        
        out["F"] = np.column_stack([-1*pi_s, -1*pi_a,-1*U])
            
        #constrains (equations are filped in a way that they would be less than zero)
        g1 = x[:,0] - (x[:,2]*self.RPM/1000)
        g2 = -1*(pi_s)
        g3 = -1*(pi_a)
        g4 = (0.8 - U)

        out["G"] = np.column_stack([g1, g2, g3, g4])


def solve_optimization_problem(problem: AdaptationProblem):
    # defining algorithm
    algorithm = NSGA2(
        pop_size=100,
        n_offsprings=10,
        eliminate_duplicates=True
    )

    # defining termination
    # i chosed termination criteria by looking at decrese in average cv
    termination = get_termination('n_gen', 170)

    # solving problem and getting the results
    res = minimize(problem,
                   algorithm,
                   termination,
                   seed=1,
                   save_history=True,
                   verbose=False
                   )

    # you can find objectives in res.F and variables in res.X
    return res.F, res.X

def choose_on_pf(pareto_f,design_space,w_s=0.33,w_a=0.33,w_u=0.33):
    max_values = np.max(pareto_f,axis=0)
    arg_max = np.argmax(pareto_f[:,0]*w_s/max_values[0] + pareto_f[:,1]*w_a/max_values[1] + pareto_f[:,2]*w_u/max_values[2])
    return tuple(design_space[arg_max])