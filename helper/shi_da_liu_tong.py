import tushare as ts
token = '5906ff18c34dff7b47f8a564b5ae483465b7be3bf1c1bafe76c73b41'
ts.set_token(token)

pro = ts.pro_api()

df = pro.top10_floatholders(ts_code='000725.SH')
print(df)