# -*- coding: utf-8 -*-
# 时间    : 2019/1/16 11:17
# 作者    : xcl
# -*- coding: utf-8 -*-
# 时间    : 2019/1/16 11:03
# 作者    : xcl


'''
                            增加经纬度计算距离
                            忽略空列表计算均值而产生的warnings
'''

#因为采集AOD时会出现缺失值，因此计算范围内均值时会出现warnings
#导入以下库来忽略该warnings
import warnings
warnings.filterwarnings('ignore')
#相关库
from math import radians, cos, sin, asin, sqrt
#import xlwt
import pandas as pd
import numpy as np
from pyhdf.SD import SD, SDC
# #import pprint
import datetime

JCZ_file = pd.read_excel("JCZ.xlsx")
JCZ = []
for i in range(len(JCZ_file)):
    JCZ1 = [JCZ_file["经度"][i],JCZ_file["纬度"][i],JCZ_file["城市"][i]+"-"+JCZ_file["监测点名称"][i]]
    exec('JCZ%s = [JCZ_file["经度"][i],JCZ_file["纬度"][i],JCZ_file["城市"][i]+"-"+JCZ_file["监测点名称"][i]]' %i)
    exec("JCZ.append(JCZ%s)" %i)
print(JCZ,len(JCZ),sep="\n")











