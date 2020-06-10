import numpy as np
from scipy import integrate


class sSpolicy:
    """
    Define a (s, S) policy class, to get the concrete stragety.
    """
    def __init__(self, pdf, alpha, leadtime, setup_cost, holding_cost,
                 monthly_demand, period=1, isInt=True):
        self.pdf = pdf
        self.alpha = alpha
        self.period = period
        self.leadtime = leadtime
        self.K = setup_cost
        self.h = holding_cost
        self.max_demand = max(monthly_demand)
        self.monthly_demand = monthly_demand
        self.isInt = isInt
        self.init()

    def init(self):
        def x_pdf(x): return self.pdf(x)*x
        # self.mu = integrate.quad(x_pdf, -np.inf, np.inf)[0]
        self.mu = sum(self.monthly_demand)/len(self.monthly_demand)
        self.coe_normalize = 1/(integrate.quad(self.pdf, 0, 10*self.max_demand)[0])
        if self.isInt:
            self.s = self.get_s() * (self.leadtime+self.period)
            self.S = self.s + (2 * self.mu * self.K / self.h) ** .5

        else:
            self.s = round(self.get_s() * (self.leadtime+self.period))
            self.S = round(self.s + (2 * self.mu * self.K / self.h) ** .5)

        self.Is = self.s - (self.leadtime+self.period)*self.mu

    def get_s(self):
        def pdf_updated(x):
            return self.pdf(x)*self.coe_normalize
        ing = 0
        x = 0
        while ing < self.alpha:
            ing = integrate.quad(pdf_updated, 0, x)[0]
            # ing = integrate.quad(self.pdf, -np.inf, x)[0]
            x += 0.1
        return x



if __name__ == "__main__":
    pass
