"""
Realize a kernel density estimate.
"""
from sklearn.neighbors import KernelDensity
import numpy as np
import pandas as pd
from function import merge_date, get_xy, get_month_demand
import matplotlib
import matplotlib.pyplot as plt


def kde(goods_category):
    """
    Do Kernel Density Estimate for monthly demand of each product 
    ------
    return `KernelDensity Object`
    """ 
    for i in [goods_category[0]]:
        good_code, time, quantity = merge_date(i)
        ser = pd.Series(quantity, index=time)
        md = get_month_demand(ser)
        X = np.array([list(range(1,13)),md]).T
        kd = KernelDensity().fit(X)
    return kd

def plot_kde(kd):
    sm = kd.sample(100)
    plot_data = np.sort(sm, axis=0)
    fig, ax = plt.subplots(2, 1)
    x = sm[:, 0]
    y = sm[:, 1]
    ax[0].plot(list(range(12)), get_month_demand(pd.Series(merge_date(goods_category[0])[2],index=merge_date(goods_category[0])[1])))
    ax[1].bar(x,y)
    plt.show()




if __name__ == "__main__":
    file_place = "/data/outbound.xlsx"
    code_name, goods_category = get_xy(file_place)
    kd = kde(goods_category)
    plot_kde(kd)
    # for i in goods_category[:1]:
    #     good_code, time, quantity = merge_date(i)
    #     x = np.array(list(range(len(time))))[:, np.newaxis]
    #     y = np.array(quantity)[:, np.newaxis]
    #     bins = np.linspace(-5, 10, 10)

    #     fig, ax = plt.subplots(2, 2, sharex=True, sharey=True)
    #     fig.subplots_adjust(hspace=0.05, wspace=0.05)


    #     # histogram 1
    #     ax[0, 0].hist(y[:, 0], bins=bins, fc='#AAAAFF')
    #     ax[0, 0].text(-3.5, 0.31, "Histogram")

    #     # histogram 2
    #     ax[0, 1].hist(y[:, 0], bins=bins + 0.75, fc='#AAAAFF')
    #     ax[0, 1].text(-3.5, 0.31, "Histogram, bins shifted")

    #     # tophat KDE
    #     kde = KernelDensity(kernel='tophat', bandwidth=0.75).fit(y)
    #     log_dens = kde.score_samples(x)
    #     ax[1, 0].fill(x[:, 0], np.exp(log_dens), fc='#AAAAFF')
    #     ax[1, 0].text(-3.5, 0.31, "Tophat Kernel Density")

    #     # Gaussian KDE
    #     kde = KernelDensity(kernel='gaussian', bandwidth=0.75).fit(y)
    #     log_dens = kde.score_samples(x)
    #     ax[1, 1].fill(x[:, 0], np.exp(log_dens), fc='#AAAAFF')
    #     ax[1, 1].text(-3.5, 0.31, "Gaussian Kernel Density")

    #     for axi in ax.ravel():
    #         axi.plot(y[:, 0], np.full(y.shape[0], -0.01), '+k')
    #         axi.set_xlim(-4, 9)
    #         axi.set_ylim(-0.02, 0.34)

    #     for axi in ax[:, 0]:
    #         axi.set_ylabel('Normalized Density')

    #     for axi in ax[1, :]:
    #         axi.set_xlabel('x')
    #     plt.show()