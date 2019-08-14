# -*- coding: utf-8 -*-
# 时间    : 2019/2/4 11:27
# 作者    : xcl



import warnings
from math import radians, cos, sin, asin, sqrt  # 经纬度计算距离
import pandas as pd  # BDS
import numpy as np  # BDS
from pyhdf.SD import SD  # 批量导入HDF
import datetime  # 程序耗时
import os  # 关机,批量文件
import time  # 关机

# 忽视空列表计算均值而导致的警告
warnings.filterwarnings('ignore')

# 开始计算耗时
start_time = datetime.datetime.now()


# 定义经纬度距离公式
def geo_distance(lng1, lat1, lng2, lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    d_lon = lng2 - lng1
    d_lat = lat2 - lat1
    a = sin(d_lat/2)**2 + cos(lat1) * cos(lat2) * sin(d_lon/2)**2
    dis = 2*asin(sqrt(a))*6371.393*1000  # 地球半径
    return dis  # 输出结果的单位为“米”

def geo_distance2(lng1, lat1, lng2, lat2):
    lng1, lat1, lng2, lat2 = map(np.radians, [lng1, lat1, lng2, lat2])
    d_lon = lng2 - lng1
    d_lat = lat2 - lat1
    a = np.sin(d_lat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(d_lon/2)**2
    dis = 2*np.arcsin(np.sqrt(a))*6371.393*1000  # 地球半径
    return dis  # 输出结果的单位为“米”

for i in range(1000):
    dis = geo_distance(i,123,234,345)-geo_distance2(i,123,234,345)
    print(dis)
end_time = datetime.datetime.now()
print(end_time-start_time)
