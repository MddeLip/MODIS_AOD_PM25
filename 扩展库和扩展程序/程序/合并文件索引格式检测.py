# -*- coding: utf-8 -*-
# 日期: 2019/3/18 23:18
# 作者: xcl
# 工具：PyCharm



import pandas as pd
import numpy as np
import os

input_file_path = "F:\\毕业论文程序\\气象数据\\整理\\日均\\"
input_file_name = os.listdir(input_file_path)  # 文件名列表
print(len(input_file_name))

for file_name in input_file_name:
    # 读取数据
    input_AOD = "F:\\毕业论文程序\\气溶胶光学厚度\\日均\\"+file_name
    input_sky = "F:\\毕业论文程序\\气象数据\\整理\\日均\\"+file_name
    input_PM = "F:\\毕业论文程序\\污染物浓度\\整理\\日均\\"+file_name
    input_temperature_mean = "F:\\毕业论文程序\\气象数据\\整理\\逐时均值\\"+file_name
    output_name = input_AOD.replace("F:\\毕业论文程序\\气溶胶光学厚度\\日均\\", "")
    output_name = output_name.replace(".xlsx", "")
    data_PM = pd.read_excel(input_PM)
    print(data_PM.iloc[1]["日期"].__class__)
    data_aod = pd.read_excel(input_AOD)
    print(data_aod.iloc[1]["日期"].__class__)
    data_sky = pd.read_excel(input_sky)
    print(data_sky.iloc[1]["日期"].__class__)
    # print(data_sky.head())
    # 这里是插入一天内气温的平均值
    data_temperature_mean = pd.read_excel(input_temperature_mean)
    print(data_temperature_mean.iloc[1]["日期"].__class__)


