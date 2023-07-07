import tushare as ts
import  stock_info as info
import pandas as pd
import logging
import numpy as np
import datetime
import os
import math
import time

token = '5906ff18c34dff7b47f8a564b5ae483465b7be3bf1c1bafe76c73b41'
ts.set_token(token)

pro = ts.pro_api()


class TopTenShareholder():

    def get_shareholder(self,stock_code,isfloat):
        if isfloat:
            print('正在处理：{}'.format(stock_code))
            shareholder = pro.top10_floatholders(ts_code=stock_code)
        else:
            shareholder = pro.top10_holders(ts_code=stock_code)
        shareholder_df = pd.DataFrame(shareholder)
        return shareholder_df


    def shareholder_increases(self,shareholder_df):
        result_year = shareholder_df.groupby('end_date')['hold_amount'].sum()
        # result = shareholder_df.groupby('end_date')
        df1 = shareholder_df.groupby(['end_date']).agg({"hold_amount": "sum"})
        shareholder_arr = np.array(result_year)
        if len(shareholder_arr) > 3:
            last1 = shareholder_arr[len(shareholder_arr) - 1]
            last2 = shareholder_arr[len(shareholder_arr) - 2]
            percent = (last1 - last2) / last2
            return percent
        return 0

    def groupby_end_date(self, df):
        buy_sig = df["hold_amount"].values.sum()

    def get_stock_list(self):
        data = pro.stock_basic(fields='ts_code,symbol,name,fullname,industry,list_date')
        return data

    def get_index_classify(self):
        classify = pro.index_classify(level='L2', src='SW2021')
        return classify

    def get_tonghuashun_classify(self):
        classify = pro.ths_index(exchange='A',type='N')
        return classify

    def test_case(self,type):
        is_ths = type == 1
        index_percent_dic = {}
        index_code_dic = {}
        if is_ths:
            classify = self.get_tonghuashun_classify()
            index_codes = classify['ts_code'].values
            index_names = classify['name'].values
        else:
            classify = self.get_index_classify()
            index_codes = classify['index_code'].values
            index_names = classify['industry_name'].values
        for index in range(len(index_codes)):
            index_code = index_codes[index]
            index_name = index_names[index]
            if is_ths:
                index_list = pro.ths_member(ts_code=index_code)['code']
            else:
                index_list = pro.index_member(index_code=index_code)['con_code']

            good_stock_dic = {}
            for code in index_list:
                if not info.is_a_market(code):
                    continue
                share_holder_df1 = self.get_shareholder(code, True)
                share_holder_df2 = self.get_shareholder(code, False)
                if len(share_holder_df1) <= 0 or len(share_holder_df2) <= 0:
                    continue
                percent1 = self.shareholder_increases(share_holder_df1)
                percent2 = self.shareholder_increases(share_holder_df2)
                if percent1 > 0 and percent2 >= 0:
                    good_stock_dic[code] = percent1
                    # if percent1 != percent2:
                    #     print("code:{},percent1:{},percent2:{}".format(code, percent1, percent2))
                # time.sleep(0.5)
                time.sleep(0.2)
            if len(good_stock_dic) > 0:
                good_stock_dic = sorted(good_stock_dic.items(), key=lambda x: x[1], reverse=True)
                index_code_dic[index_name] = good_stock_dic
                index_percent = len(good_stock_dic) / len(index_list)
                index_percent_dic[index_name] = index_percent
                if index_percent > 0.5:
                    print(
                        '当前行业：{},行业名称:{},个数:{},百分比:{},股票列表:{}'.format(index_code, index_name, len(index_list),index_percent,
                                                                               good_stock_dic))
        index_percent_dic = sorted(index_percent_dic.items(), key=lambda x: x[1], reverse=True)
        print('行业排序：{}'.format(index_percent_dic))
        for index_temp in index_percent_dic:
            print('所属行业:{},百分比:{},入选个数:{}，个股排名:{}'.format(index_temp[0], index_temp[1],len(index_code_dic[index_temp[0]]), index_code_dic[index_temp[0]]))

if __name__ == '__main__':
    model = TopTenShareholder()
    model.test_case(1)
    # code = '001313.SZ'
    # share_holder_df1 = model.get_shareholder(code, True)
    # share_holder_df2 = model.get_shareholder(code, False)
    # percent1 = model.shareholder_increases(share_holder_df1)
    # percent2 = model.shareholder_increases(share_holder_df2)
    # aaa = {}
    # aaa['00001'] = 0.1
    # aaa['000019'] = 0.2
    # aaa['000018'] = 0.3
    # aaa = sorted(aaa.items(), key=lambda x: x[1], reverse=True)
    # for a in aaa:
    #     print(a)



