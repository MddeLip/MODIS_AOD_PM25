# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/7/5 18:01

import numpy as np
import pandas as pd
from datetime import datetime as dt  # 时间戳日期转换
import datetime  # 程序耗时
import time

# 读取
#data = pd.read_excel("D:\\毕业论文程序\\MODIS\\建模\\基于新数据格式\\相邻位置仅留PM和T-1.xlsx")
data = pd.read_excel("D:\\毕业论文程序\\MODIS\\建模\\基于新数据格式\\自身与相邻站点PM_AOD_T-1_全样本.xlsx")
#data = pd.read_excel("D:\\毕业论文程序\\MODIS\\建模\\基于新数据格式\\测试用数据.xlsx")



#data['year'] =data['日期'].map(lambda x: time.strptime(x, "%Y-%m-%d %H:%M:%S"))
# 已经是字符串了，不是日期格式
data["year"] = data["日期"].map(lambda x: x[0:4])

print(data["year"])
