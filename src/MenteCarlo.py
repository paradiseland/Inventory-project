import random
import math


class MonteCarlo:
    """
    Define a montecarlo class to get the integrate of complex f(x).
    """
    def __init__(self, pdf, upperbound, lowerbound=0, sim_times=10000):
        self.pdf = pdf
        self.upperbound = upperbound
        self.lowerbound = lowerbound
        self.sim_times = sim_times

    def integrate(self):
        sum_ = 0
        count = 1
        while count <= self.sim_times:
            sum_ += self.pdf(random.uniform(self.lowerbound, self.upperbound))
            count += 1
        return (self.upperbound-self.lowerbound)*(sum_/self.sim_times)


if __name__ == "__main__":
    def f_x_(x):
        return 3*(x**2)+4*math.cos(x)-4*x*math.sin(x)

    print(MonteCarlo(f_x_, 15, 10).integrate())
