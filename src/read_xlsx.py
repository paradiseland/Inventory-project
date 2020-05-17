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


class 

if __name__ == "__main__":
    outbound_file = os.getcwd()+"/data/outbound.xlsx"
    outbound = Outbound(outbound_file)
    outbound.get_value_counts(outbound.column)
    print(outbound.category)
