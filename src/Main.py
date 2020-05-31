from Plan import Plan, sSPlan
from Kde import KDE
from sS_policy import sSpolicy

if __name__ == "__main__":
    outbound_filename = "outbound.xlsx"
    initinv_filename = "init_inventory.xlsx"
    plan = Plan(outbound_filename, initinv_filename)
    price = plan.price
    dict_code2name = plan.code_name
    monthly_demand_all = plan.get_monthly_demand()[0]
    sS_record = dict()
    for code, monthly_demand in monthly_demand_all.items():
        kde = KDE(code, monthly_demand)
        # fig, ax = plt.subplots(2)
        print(dict_code2name[code]+":")
        # TODO:
        # FIXME:
        #

        # pdf = kde.pdf
        # x_p = np.linspace(np.min(kde.demand), np.max(kde.demand), 300)
        # y_p = [pdf.subs(x, x_i) for x_i in x_p]
        # ax[0].plot(x_p, y_p)
        # kde.plot()
        # print(kde.estimate.score(kde.demand))
        sS = sSpolicy(kde.pdf, alpha=.9, leadtime=2, setup_cost=100,
                      holding_cost=.05*price[code],
                      monthly_demand=monthly_demand)
        print('mu', sS.mu)
        print("s:{}, S:{}".format(sS.s, sS.S))
        sS_record[code] = [sS.s, sS.S]
        # break
    print(sS_record)
    sSplan = sSPlan(outbound_filename, initinv_filename, sS_record)
    print(sSplan.get_plan())
