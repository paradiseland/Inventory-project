import os
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters


def merge_date(df):
    """
    merge the same goods on the same day.  
    """
    res = df.groupby(['物料编码', '出库单输入日期'])['实发数量'].apply(list)
    good_code = res.index[0][0]
    return good_code, res.index.levels[1], [sum(i) for i in res.values]


def get_map(multi_df):
    """
    generate a map from good code to good name.
    """
    code_name = dict()
    for i in multi_df:
        tmp = str(i.iloc[0, 0])
        code_name[tmp] = i.iloc[0, 1]

    return code_name

def get_xy(file_place):
    """
    from excel file, get the time and demand.
    """
    from read_xlsx import Outbound
    register_matplotlib_converters()
    outbound_file = os.getcwd()+file_place
    outbound = Outbound(outbound_file)
    goods_category = outbound.category
    code2name = get_map(goods_category)

    return code2name, goods_category

def get_month_demand(series):
    """
    generate the mothly demand.
    """
    monthly_demand = []
    for i in range(1,13):
        tmp = '2019/{}'.format(i)
        try:
            this_month = sum(series.loc[tmp])
            monthly_demand.append(this_month)
        except KeyError as ks:
            monthly_demand.append(0)

    return monthly_demand

def plot_demand(goods_category):
    """
    plot the demand of goods in different categories.
    1. daily demand 2. histogram
    """
    register_matplotlib_converters()
    plt.rcParams['font.family'] = ['Arial Unicode MS']  # 用来正常显示中文标签
    for i in goods_category:
        good_code, time, quantity = merge_date(i)
        ser_day = pd.Series(quantity, index=time)
        md = get_month_demand(ser_day)
        ser_mon = pd.Series(md, index = pd.period_range('1/1/2019', '12/1/2019', freq='M'))

        # we can index it by ser.loc['2019'], ser.loc['2019/5']
        dpi = 100
        xinch = 1366/dpi
        yinch = 768/dpi
        fig, ax = plt.subplots(2, 3, figsize=(xinch, yinch))
        
        ax[0, 0].plot(time, quantity)
        ax[0, 0].set_title(code_name[str(good_code)][:5]+'---daily demand') 

        ax[0, 1].bar(time, quantity)
        ax[0, 1].set_title(code_name[str(good_code)][:5]+'———[daily]---histogram')
        
        plt.sca(ax[0,2])
        ser_day.plot(kind='kde')
        ax[0, 2].set_title('Kernel density figure ---daily')


        ax[1, 0].plot(list(range(12)), md)
        ax[1, 0].set_title(code_name[str(good_code)][:5]+'---monthly demand')
        
        ax[1, 1].bar(list(range(12)), md)
        ax[1, 1].set_title(code_name[str(good_code)][:5]+'———[monthly]---histogram')
        
        plt.sca(ax[1,2])
        ser_mon.plot(kind='kde')
        ax[1, 2].set_title('Kernel density figure ---monthly')
        
        for i in range(2):
            ax[0,i].set_xticks(time)
            ax[0,i].set_xticklabels('|')
        
            ax[1, i].set_xticks(list(range(12)))
            ax[1, i].set_xticklabels([str(i)+'月' for i in list(range(1,13))])

        plt.grid(True)
        # plt.savefig(f'./result/{code_name[str(good_code)][:5]}.png', format='png', quality=90, dpi=300)
        # plt.show()

if __name__ == "__main__":
    file_place = "/data/outbound.xlsx"
    code_name, goods_category = get_xy(file_place)
    plot_demand(goods_category)
