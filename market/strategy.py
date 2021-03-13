import requests
import json
import pandas as pd
import datetime

def convert_float(x):
    try:
        ret_float = float(x)
        # format(ret_float, '.2f')
        "{:10.0f}".format(ret_float)
    except:
        ret_float = None
    return ret_float

def convert_percent(x):
    try:
        ret = float(x) * 100
    except:
        ret = None
    return ret

def remove_percent(x):
    try:
        ret = x.replace(r'%', '')
        ret = float(ret)
    except Exception as e:
        ret = None
    return ret

# "https://www.jisilu.cn/data/cbnew/cb_list/"
# 集思录数据源
response = json.loads(requests.get(cfg.JSL_HOME).text)

bond_list = response["rows"]
cell_list = []
for item in bond_list:
    #print(pd.Series(item.get('cell')))
    cell_list.append(pd.Series(item.get('cell')))
df = pd.DataFrame(cell_list)



# 类型转换 部分含有%

df['premium_rt'] = df['premium_rt'].map(lambda x: float(x.replace('%', '')))
df['price'] = df['price'].astype('float64')
df['convert_price'] = df['convert_price'].astype('float64')
df['premium_rt'] = df['premium_rt'].astype('float64')
df['redeem_price'] = df['redeem_price'].astype('float64')

# df['turnover_rt'] = df['turnover_rt'].map(lambda x: float(x.replace('%', '')))
df['turnover_rt'] = df['turnover_rt'].astype('float64')

df['put_convert_price'] = df['put_convert_price'].map(convert_float)
df['sprice'] = df['sprice'].map(convert_float)
df['ration'] = df['ration'].map(convert_percent)
df['volume'] = df['volume'].map(convert_float)
df['convert_amt_ratio'] = df['convert_amt_ratio'].map(remove_percent)
df['ration_rt'] = df['ration_rt'].map(convert_float)
df['increase_rt'] = df['increase_rt'].map(remove_percent)
df['sincrease_rt'] = df['sincrease_rt'].map(remove_percent)
df['curr_iss_amt'] = df['curr_iss_amt'].map(convert_float)

# print(df.columns)

# 原始集思录数据
# df.to_excel("origin.xlsx")

# 过滤掉可交换债
df = df[df.btype != 'E']

# print(df)

rename_columns = {'bond_id': '可转债代码', 'bond_nm': '可转债名称', 'price': '可转债价格', 'stock_nm': '正股名称',
                  'stock_cd': '正股代码',
                  'sprice': '正股现价',
                  'sincrease_rt': '正股涨跌幅',
                  'convert_price': '最新转股价', 'premium_rt': '溢价率', 'increase_rt': '可转债涨幅',
                  'put_convert_price': '回售触发价', 'convert_dt': '转股起始日',
                  'short_maturity_dt': '到期时间',
                  'volume': '成交额',
                  'turnover_rt': '换手率',
                  "redeem_flag" : "redeem_flag",
                  'redeem_price': '强赎价格', 'year_left': '剩余时间',
                  'next_put_dt': '回售起始日', 'rating_cd': '评级',
                  # 'issue_dt': '发行时间',
                  # 'redeem_tc': '强制赎回条款',
                  # 'adjust_tc': '下修条件',
                  'adjust_tip': '下修提示',
                  # 'put_tc': '回售',
                  'adj_cnt': '下调次数',
                  #   'ration':'已转股比例'
                  'convert_amt_ratio': '转债剩余占总市值比',
                  'curr_iss_amt': '剩余规模', 'orig_iss_amt': '发行规模',
                  'ration_rt': '股东配售率',
                  }

df = df.rename(columns=rename_columns)
df = df[list(rename_columns.values())]
df['更新日期'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

df = df.set_index('可转债代码', drop=True)