"""
Realize a kernel density estimate.
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
from Plan import Plan
from MonteCarlo import MonteCarlo


class KDE:
    """
    choose Gaussian kernel, and optimal its bandwidth
    """
    def __init__(self, code, demand):
        self.code = code
        self.demand = np.array(demand)[:, np.newaxis]
        self.estimate = KernelDensity(
            kernel='gaussian', bandwidth=self.thumb_bandwidth).fit(self.demand)

    @property
    def thumb_bandwidth(self):
        return 1.06*np.std(self.demand, ddof=1)*(len(self.demand))**(-1/5)

    def plot(self):
        X_plot = np.linspace(np.min(self.demand), np.max(
            self.demand), 300)[:, np.newaxis]
        log_dens = self.estimate.score_samples(X_plot)
        plt.fill(X_plot[:, 0], np.exp(log_dens), fc='#AAAAFF')
        plt.show()

    def pdf(self, x):
        """
        the probability density function is 1/nh*Sigma_i^n K(x-x_i)/h
        """
        n = len(self.demand)
        function = 1/(n*self.thumb_bandwidth)*sum([1/((2*np.pi)**.5)*np.e**(
            (-1/2)*((x-i[0])/self.thumb_bandwidth)**2) for i in self.demand])
        return function


if __name__ == "__main__":
    outbound_filename = "outbound.xlsx"
    initinv_filename = "init_inventory.xlsx"
    plan = Plan(outbound_filename, initinv_filename)
    dict_code2name = plan.code_name
    monthly_demand_all = plan.get_monthly_demand()[0]
    for code, monthly_demand in monthly_demand_all.items():
        kde = KDE(code, monthly_demand)
        fig, ax = plt.subplots(2)
        print(monthly_demand)
        print(sum(monthly_demand)/len(monthly_demand))
        pdf = kde.pdf
        x_p = np.linspace(np.min(kde.demand), np.max(kde.demand), 300)
        y_p = [pdf(x_i) for x_i in x_p]
        ax[0].plot(x_p, y_p)
        kde.plot()
        # print(kde.estimate.score(kde.demand))
        print(MonteCarlo(kde.pdf, lowerbound=0, upperbound=1.5 *
                         max(monthly_demand), sim_times=10000).get_mu())
        print(MonteCarlo(kde.pdf, lowerbound=0, upperbound=1.5 *
                         max(monthly_demand), sim_times=10000).get_F_eq_alpha(.8, 3))
        break
