import sympy
from MenteCarlo import MonteCarlo


class sSpolicy:
    """
    Define a (s, S) policy class, to get the concrete stragety.
    """
    def __init__(self, pdf, alpha, leadtime, setup_cost, holding_cost,
                 period=1):
        self.pdf = pdf
        self.alpha = alpha
        self.period = period
        self.leadtime = leadtime
        self.K = setup_cost
        self.h = holding_cost
        self.max_demand = 
        self.init()

    def init(self):
        def x_pdf(x): return self.pdf(x)*x
        self.mu = MonteCarlo(x_pdf, upperbound=1.5*self.max_demand).integrate()
        self.s = self.get_s()
        self.S = self.s + (2 * self.mu * self.K / self.h) ** .5
        self.Is = self.s - (self.leadtime+self.period)*self.mu

    def get_s(self):
        # TODO:
        f_A_L = self.pdf * (self.period+self.leadtime)

        return s


if __name__ == "__main__":
    pass
