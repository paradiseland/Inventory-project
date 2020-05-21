"""
Compute the cost of original plan 
-----------------------
plan:

"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters


class Plan:
    def __init__(self, outbound_name, ininv_name):
        self.leadtime = 2
        self.period = 1
        self.setup_cost = 100
        self.hold_cost_coe = .05
        self.penalty = self.hold_cost_coe * 10
        self.category = self.outbound_demo(outbound_name)
        self.init_inventory = self.init_inv(ininv_name)
        self.monthly_demand, self.ser_days, self.code = self.get_monthly_demand()

    def outbound_demo(self, file_name):
        """
        class dataframe into different catagories by its goods code.
        """
        outbound_file = os.getcwd()+"/data/"+file_name
        self.df = pd.read_excel(outbound_file)
        df_all = []
        goods_coding = self.df.iloc[:, 0].unique()
        for catagory in goods_coding:
            tmp_data = self.df[self.df.iloc[:, 0].isin([catagory])]
            df_all.append(tmp_data)
        return df_all

    def init_inv(self, file_name):
        """
        return dict of code and initial inventory.
        """
        initinv_file = os.getcwd()+"/data/"+file_name
        self.inv = pd.read_excel(initinv_file)
        return dict(zip(self.inv["物料编码"].tolist(), self.inv["库存数量"].tolist()))

    @property
    def price(self):
        code = []
        price = []
        for good in self.category:
            code.append(good.iloc[0,0])
            price.append(good["单价"].mean())
        return dict(zip(code, price))

    def get_monthly_demand(self):
        """
        generate the mothly demand.
        """
        code = []
        demand = []
        ser_days = []
        for good in self.category:
            code.append(good.iloc[0, 0])
            monthly_demand = []
            tmp = good.groupby(['物料编码', '出库单输入日期'])['实发数量'].apply(list)
            ser_day = pd.Series([sum(i) for i in tmp.values],  index= tmp.index.levels[1])
            for i in range(1,13):
                tmp = '2019/{}'.format(i)
                try:
                    this_month = sum(ser_day.loc[tmp])
                    monthly_demand.append(this_month)
                except KeyError:
                    monthly_demand.append(0)
            ser_days.append(ser_day)
            demand.append(monthly_demand)

        return dict(zip(code, demand)), dict(zip(code, ser_days)), code

    @property
    def code_name(self):

        """
        generate a map from good code to good name.
        """
        code_name = dict()
        for i in self.category:
            tmp = i.iloc[0, 0]
            code_name[tmp] = i.iloc[0, 1]
        return code_name

    @property
    def quota(self):
        code = []
        quota = []
        for i in self.category:
            code.append(i.iloc[0,0])
            quota.append(i.iloc[0,8])
        return dict(zip(code, quota))

    def plot_monthly_demand(self):
        """
        plot the demand of goods in different categories.
        1. daily demand 2. histogram
        """
        register_matplotlib_converters()
        plt.rcParams['font.family'] = ['Arial Unicode MS']  # 用来正常显示中文标签
        for i in self.code:
            ser_day = self.ser_days[i]
            ser_mon = pd.Series(self.monthly_demand[i], index = pd.period_range('1/1/2019', '12/1/2019', freq='M'))
            time = ser_day.index
            quantity = ser_day.values
            dpi = 100
            xinch = 1366/dpi
            yinch = 768/dpi
            fig, ax = plt.subplots(2, 3, figsize=(xinch, yinch))
            ax[0, 0].plot(time, quantity)
            ax[0, 0].set_title(self.code_name[str(i)][:5]+'---daily demand') 

            ax[0, 1].bar(time, quantity)
            ax[0, 1].set_title(self.code_name[str(i)][:5]+'———[daily]---histogram')

            plt.sca(ax[0,2])
            ser_day.plot(kind='kde')
            ax[0, 2].set_title('Kernel density figure ---daily')

            ax[1, 0].plot(list(range(12)), ser_mon.values)
            ax[1, 0].set_title(self.code_name[str(i)][:5]+'---monthly demand')

            ax[1, 1].bar(list(range(12)), ser_mon.values)
            ax[1, 1].set_title(self.code_name[str(i)][:5]+'———[monthly]---histogram')

            plt.sca(ax[1, 2])
            ser_mon.plot(kind='kde')
            ax[1, 2].set_title('Kernel density figure ---monthly')

            for i in range(2):
                ax[0, i].set_xticks(time)
                ax[0, i].set_xticklabels('|')

                ax[1, i].set_xticks(list(range(12)))
                ax[1, i].set_xticklabels(
                    [str(i)+'月' for i in list(range(1, 13))])

            plt.grid(True)
            # plt.savefig(f'./result/{code_name[str(good_code)][:5]}.png',
            #             format='png', quality=90, dpi=300)
            plt.show()


class OriginalPlan(Plan):

    def __init__(self, outbound_name, ininv_name):
        super().__init__(outbound_name, ininv_name)
        self.s_coe = 1/2

    def get_plan(self):
        """
        月初到货,月初盘点
        """
        order_all = []
        inventory_all = []
        for good in self.code:
            demand = self.monthly_demand[good]
            quot = self.quota[good]

            order = [0]*14  # 2018/11-2019/12: 14 month
            inventory_real = [self.init_inventory[good]]+[0]*13  # 2019/1-2020/2:14 month
            inventory_will = [self.init_inventory[good]]+[0]*13
            month = 0

            while month < 12:
                if inventory_will[month] < quot/2:
                    order[month+2] = quot - inventory_will[month]

                else:
                    order[month+2] = 0

                inventory_real[month+1] = inventory_real[month] - demand[month] + order[month+1]
                inventory_will[month+1] = inventory_will[month]-demand[month] + order[month+2]
                month += 1
            order_all.append(order)
            inventory_all.append([inventory_real, inventory_will])
        return order_all, inventory_all


    def compute_cost(self):
        order_all, inventory_all = self.get_plan()
        cost = dict()
        for ind, good in enumerate(self.code):
            tmp = 0
            order = order_all[ind]
            inventory_real = inventory_all[ind][0]
            for inv_mon,orde in zip(inventory_real[:12], order[2:]):
                if inv_mon > 0:
                    tmp += self.hold_cost_coe*self.price[good]
                else:
                    tmp += self.penalty*self.price[good]
                if orde > 0:
                    # tmp += self.setup_cost + orde * self.price[good]
                    tmp += self.setup_cost
            cost[good] = tmp
        return cost


if __name__ == "__main__":
    outbound_filename = "outbound.xlsx"
    initinv_filename = "init_inventory.xlsx"
    ori = OriginalPlan(outbound_filename, initinv_filename)
    # ori.plot_monthly_demand()
