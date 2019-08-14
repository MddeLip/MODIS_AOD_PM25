# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/7/11 13:38

import os
import pandas as pd
import warnings
from datetime import datetime as dt
import datetime
import time

# 参数设置
input_file_path = "D:\\下载\\城市_20190101-20190706\\"
input_file_name = os.listdir(input_file_path)  # 文件名
output_file_path = "D:\\TOJMD\\"
error_path = "D:\\毕业论文程序\\污染物浓度\\error\\"

# 主程序

res = []
for file in input_file_name:
    # print(file)
    date = file.replace("china_cities_", "").replace(".csv", "")
    #date = file.replace("beijing_all_", "").replace(".csv", "")  # 适用于北京
    # date = file.replace("china_cities_", "").replace(".csv", "")
    date = time.strptime(date, '%Y%m%d')
    date = time.strftime("%Y-%m-%d", date)
    date = dt.strptime(date, '%Y-%m-%d').date()
    print(file)
    data = pd.read_csv(input_file_path + file, encoding='utf8')

    data = data[(data['type'] == "PM2.5_24h") & (data["hour"] == 0)]
    res.append(data)


data_res = pd.concat(res, axis=0)
print(data_res)


def get_day(date_input, step=0):
    """获取指定日期date(形如"xxxxxxxx")之前或之后的多少天的日期, 返回值为字符串格式的日期"""
    date_input = str(date_input)  # 转化为字符串方便合并
    date_input = date_input[0:4]+"-"+date_input[4:6]+"-"+date_input[6:8]
    l_input = date_input.split("-")
    y = int(l_input[0])
    m = int(l_input[1])
    d = int(l_input[2])
    old_date = datetime.datetime(y, m, d)
    new_date = (old_date + datetime.timedelta(days=step)).strftime('%Y-%m-%d')
    # print(new_date)
    return new_date


data_res["date"] = data_res["date"].map(lambda x: get_day(x, -1))  # 今日的0时PM2.5_24h对应前一天PM2.5日均值
data_res = data_res.drop(["hour"], axis=1)

data_res.to_excel("jmd.xlsx")


