from Plan import Plan, sSPlan, OriginalPlan
from Kde import KDE
from sS_policy import sSpolicy
import matplotlib.pyplot as plt


def plot_comp(dic1, dic2):
    plt.bar(range(len(dic1)), list(dic1.values()), color='#4682B4', width=0.4)
    plt.bar([i+0.4 for i in range(len(dic2))], list(dic2.values()), color='#D2691E', width=0.4)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    outbound_filename = "outbound.xlsx"
    initinv_filename = "init_inventory.xlsx"
    plan = Plan(outbound_filename, initinv_filename)
    price = plan.price
    dict_code2name = plan.code_name
    monthly_demand_all = plan.get_monthly_demand()[0]
    isInt = plan.isInt
    sS_record = dict()
    ori = OriginalPlan(outbound_filename, initinv_filename)
    for code, monthly_demand in monthly_demand_all.items():
        kde = KDE(code, monthly_demand)
        # print(code, ori.get_service_level(code, kde.pdf))
        # fig, ax = plt.subplots(2)
        # print(dict_code2name[code]+":")

        # pdf = kde.pdf
        # x_p = np.linspace(np.min(kde.demand), np.max(kde.demand), 300)
        # y_p = [pdf.subs(x, x_i) for x_i in x_p]
        # ax[0].plot(x_p, y_p)
        # kde.plot()
        # print(kde.estimate.score(kde.demand))
        IsInt = isInt[code]
        sS = sSpolicy(kde.pdf, alpha=.9, leadtime=2, setup_cost=100,
                      holding_cost=.05*price[code],
                      monthly_demand=monthly_demand, isInt=IsInt)
        # print('mu', sS.mu)
        # print("s:{}, S:{}".format(sS.s, sS.S))
        sS_record[code] = [sS.s, sS.S]

        # break
    print(sS_record)
    print(plan.code_name)
    sSplan = sSPlan(outbound_filename, initinv_filename, sS_record)
    print(sSplan.estimate())
    print(sSplan.get_plan())
    print(sSplan.compute_cost())
    # ori.plot_monthly_demand()
    print(ori.get_plan())
    print(ori.compute_cost())
    plot_comp(sSplan.compute_cost(), ori.compute_cost())



