import random
import math
import numpy as np
from scipy import integrate


class MonteCarlo:
    """
    Define a montecarlo class to get the integrate of complex f(x).
    """
    def __init__(self, pdf, upperbound, lowerbound=0):
        self.pdf = pdf
        self.upperbound = upperbound
        self.lowerbound = lowerbound

    def get_mu(self):
        def x_pdf(x):
            return self.pdf(x)*x
        return integrate.quad(x_pdf, self.lowerbound, self.upperbound)[0]

    def get_F_eq_alpha(self, alpha, a_l):
        ing = 0
        while ing < alpha:
            ing = integrate.quad(self.pdf, self.lowerbound, self.upperbound)[0]
            self.upperbound += 1
        return self.upperbound


if __name__ == "__main__":
    def f_x_(x):
        return 3*(x**2)+4*math.cos(x)-4*x*math.sin(x)

    print(MonteCarlo(f_x_, 15, 10).get_mu())