import pandas as pd
import os


class Outbound:
    def __init__(self, out_file):
        self.df = pd.read_excel(out_file)
    
    @property
    def column(self):
        return self.df.columns

    def get_value_counts(self, column_name):
        """
        input list-like object, return the list output of value_counts().
        """
        res = []
        for i in column_name:
            res.append(self.df[i].value_counts())
        print(res)
        return res
        
    @property
    def category(self):
        """
        class dataframe into different catagories by its goods code.
        """
        df_all = []
        goods_coding = self.df.iloc[:, 0].unique()
        for catagory in goods_coding:
            tmp_data = self.df[self.df.iloc[:, 0].isin([catagory])]
            df_all.append(tmp_data)
        return df_all


class Init_inventory:
    def __init__(self, initinv_file):
        self.df = pd.read_excel(initinv_file)

    def get_init_inventory(self):
        """
        return dict of code and initial inventory.
        """
        return  dict(zip(self.df["物料编码"].tolist(), self.df["库存数量"].tolist()))

if __name__ == "__main__":
    outbound_file = os.getcwd()+"/data/outbound.xlsx"
    init_file = os.getcwd()+"/data/init_inventory.xlsx"
    outbound = Outbound(outbound_file)
    init_inv = Init_inventory(init_file)
    print(init_inv.get_init_inventory())
