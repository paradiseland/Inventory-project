import sympy


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
        self.init()

    def init(self):
        self.mu = sympy.integrate(self.pdf, (x, 0, sympy.oo))
        self.s = self.get_s()
        self.S = self.s + (2 * self.mu * self.K / self.h) ** .5
        self.Is = self.s - (self.leadtime+self.period)*self.mu

    def get_s(self):
        # TODO:
        f_A_L = self.pdf * (self.period+self.leadtime)

        return s


if __name__ == "__main__":
    pass
