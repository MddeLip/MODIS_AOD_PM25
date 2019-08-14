# -*- coding: utf-8 -*-
# 日期: 2019/3/18 22:08
# 作者: xcl
# 工具：PyCharm

# 均值应为 1-24时均值


import pandas as pd
import datetime
from datetime import datetime as dt
import os

# 批量读取


input_path = "D:\\毕业论文程序\\气象数据\\数据\\逐时\\2017\\"
output_path = "D:\\毕业论文程序\\气象数据\\整理\\逐时均值\\2017\\"
file_name_list = os.listdir(input_path)  # 文件名

for name in file_name_list:
    print("整理" + name + "中")
    file_name = name.replace(".xlsx", "")
    data = pd.read_excel(input_path + name)
    data["Index"] = data["time"]
    data = data.set_index('Index')
    # 将时间序列转换为指定的频率
    data = data.asfreq(freq='60min')
    data["time"] = data.index  # 补全信息,这个方法以后可能会经常使用到
    for key in data.columns:
        data["%s" % key] = data["%s" % key].interpolate()  # 线性填充
    '''
    for key in data.columns:
        data["%s" % key] = data["%s" % key].fillna(method='ffill')
    '''
    data["日期"] = data["time"]  # 新建日期列 之后添加.dt.date
    data["time_only"] = data["time"].dt.time  # 时间列只保留时间

    # 如果把1-24 转换为0-23 则可以使用 data = data.groupby("日期").mean()

    def get_new_time(x):
        x = x + datetime.timedelta(hours=-1)
        return x
    data["日期"] = data["日期"].map(lambda x: get_new_time(x))  # 今日的0时PM2.5_24h对应前一天PM2.4日均值,即1-24均值
    # print(data['日期'])
    data["日期"] = data["日期"].dt.date
    data["日期"] = data["日期"].map(lambda x: str(x))
    data = data.groupby("日期").mean()
    data.to_excel(output_path + "%s.xlsx" % file_name)




