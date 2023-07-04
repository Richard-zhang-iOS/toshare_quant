import tushare as ts
import  stock_info as info
token = '5906ff18c34dff7b47f8a564b5ae483465b7be3bf1c1bafe76c73b41'
ts.set_token(token)

pro = ts.pro_api()

stock_code = info.add_stocksuffix("000725")
df = pro.top10_floatholders(ts_code=stock_code)
print(df)