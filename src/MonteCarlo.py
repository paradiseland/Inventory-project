import random
import math
import numpy as np


class MonteCarlo:
    """
    Define a montecarlo class to get the integrate of complex f(x).
    """
    def __init__(self, pdf, upperbound, lowerbound=0, sim_times=10000):
        self.pdf = pdf
        self.upperbound = upperbound
        self.lowerbound = lowerbound
        self.sim_times = sim_times

    def get_mu(self):
        sum_ = 0
        count = 1
        def xf(x): return self.pdf(x)*x
        while count <= self.sim_times:
            sum_ += xf(random.uniform(self.lowerbound, self.upperbound))
            count += 1
        # for i in np.linspace(0, stop=self.upperbound, num=self.sim_times):
        #     sum_ += xf(i)
        return (self.upperbound-self.lowerbound)*(sum_/self.sim_times)

    def get_F_eq_alpha(self, alpha, a_l):
        """
        al is the sum of leadtime and pandian time.
        """
        s = []
        sum_ = 0
        i = 0
        F = 0
        x = np.linspace(start=0, stop=self.upperbound, num=self.sim_times)
        while F < alpha:
            sum_ += self.pdf(x[i])
            F = (self.upperbound-self.lowerbound)*(sum_/self.sim_times)
            i += 1
            s.append(x[i-1])

        return x[i-1]*a_l


if __name__ == "__main__":
    def f_x_(x):
        return 3*(x**2)+4*math.cos(x)-4*x*math.sin(x)

    print(MonteCarlo(f_x_, 15, 10).get_mu())
