# -*- coding: utf-8 -*-
# 时间    : 2019/1/14 21:16
# 作者    : xcl

import math
import pandas as pd
import xlwt
import pandas as pd
import numpy as np
from pyhdf.SD import SD, SDC
import pprint

HDF_FILR_URL = "1011-1.hdf"
file = SD(HDF_FILR_URL)

print(file.info())

datasets_dic = file.datasets()

for idx, sds in enumerate(datasets_dic.keys()):
    print(idx, sds)

sds_obj1 = file.select('Longitude')  # select sds
sds_obj2 = file.select('Latitude')  # select sds
sds_obj3 = file.select('Optical_Depth_Land_And_Ocean')  # select sds
longitude = sds_obj1.get()  # get sds data
latitude = sds_obj2.get()  # get sds data
aod = sds_obj3.get()  # get sds data

longitude = pd.DataFrame(longitude)
latitude = pd.DataFrame(latitude)
aod = pd.DataFrame(aod)

#print(longitude.shape[1]) #矩阵大小

#print(aod[2][1])

for i in range(longitude.shape[0]):
    for j in range(longitude.shape[1]):
        d = ((longitude[i][j])**2-118**2+(latitude[i][j])**2-39**2)#距离
    print(d)