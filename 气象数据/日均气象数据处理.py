# -*- coding: utf-8 -*-
# 日期: 2019/5/13 18:31
# 作者: xcl
# 工具：PyCharm

import pandas as pd
import datetime
from datetime import datetime as dt
import os

# 批量读取

for year_tag in range(2017, 2018):
    print(year_tag)
    input_path = "D:\\毕业论文程序\\气象数据\\数据\\日均\\%s\\" % year_tag
    output_path = "D:\\毕业论文程序\\气象数据\\整理\\日均\\%s\\" % year_tag
    file_name_list = os.listdir(input_path)  # 文件名

    for name in file_name_list:
        print("整理" + name + "中")
        file_name = name.replace(".xlsx", "")
        data = pd.read_excel(input_path + name)
        # print(data.head())
        data["Index"] = data["time"]
        data = data.set_index('Index')
        # 将时间序列转换为指定的频率
        data = data.asfreq(freq='1440min')  # 补全信息,这个方法以后可能会经常使用到
        data["time"] = data.index
        data["日期"] = data["time"].dt.date  # 新建日期列
        data["日期"] = data["日期"].map(lambda x: str(x))  # 改成字符串格式 方便日后合并
        data = data.set_index('日期')
        data = data.drop(["time"], axis=1)  # 日均条件下删除无关列

        # 日均数据,填充
        try:
            data["precipAccumulation"] = data["precipAccumulation"][data["precipType"] == "snow"].interpolate()
        except Exception as e:
            print("错误信息", e)
        try:
            data["precipIntensity"] = data["precipIntensity"][data["precipType"] == "rain"].interpolate()
        except Exception as e:
            print("错误信息", e, "\n")
        # 保存
        data.to_excel(output_path + "%s.xlsx" % file_name)
        '''
        for key in data.columns:
            data["%s" % key] = data["%s" % key].interpolate()  # 线性填充
    
        for key in data.columns:
            data["%s" % key] = data["%s" % key].fillna(method='ffill')
    
        data["日期"] = data["time"].dt.date  # 新建日期列
        data["time_only"] = data["time"].dt.time  # 时间列只保留时间
        '''

