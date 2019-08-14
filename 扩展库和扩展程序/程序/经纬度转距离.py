# -*- coding: utf-8 -*-
# 时间    : 2019/1/17 16:07
# 作者    : xcl
'''
计算发现 单元格之间最小距离3KM
'''
from math import radians, cos, sin, asin, sqrt#经纬度计算距离
def geodistance(lng1,lat1,lng2,lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlon=lng2-lng1
    dlat=lat2-lat1
    a=sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    dis=2*asin(sqrt(a))*6371.393*1000#地球半径
    return(dis)#输出结果的单位为“米”
d=geodistance(150.54767,36.397060,150.54466,36.360153)#横着
d2=geodistance(150.88062,36.176189,150.87798,36.230282)#竖着
print(d,d2)