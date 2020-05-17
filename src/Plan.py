"""
Compute the cost of original plan 
-----------------------
plan:

"""
import os
import pandas as pd
 
class Plan:
    def __init__(self, outbound_name, ininv_name):
        self.leadtime = 2
        self.period = 1
        self.setup_cost = 100
        self.hold_cost_coe = .05
        self.category = self.outbound_demo(outbound_name)
        self.init_inventory = self.init_inv(ininv_name)
        self.price = self.get_price()

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

    def get_price(self):
        code = []
        price = []
        for good in self.category:
            code.append(good.iloc[0,0])
            price.append(good["单价"].mean())
        return dict(zip(code, price))

class OriginalPlan(Plan):

    def __init__(self, outbound_name, ininv_name):
        super().__init__(outbound_name, ininv_name)
        self.s_coe = 1/2





if __name__ == "__main__":
    outbound_filename = "outbound.xlsx"
    initinv_filename = "init_inventory.xlsx"
    ori = OriginalPlan(outbound_filename, initinv_filename)
    print(ori.init_inventory, ori.category, ori.price)
