
# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/7/1 15:23

from osgeo import gdal

file_path = "D:\\MODIS\\MCD19A2_1km_2015\\"
file = file_path+"MCD19A2.A2015023.h23v05.006.2018101234406.hdf"


dataset = gdal.Open(file)

adfGeoTransform = dataset.GetGeoTransform()

print(adfGeoTransform[0])
print(adfGeoTransform[3])
nXSize = dataset.RasterXSize  # 列数
nYSize = dataset.RasterYSize  # 行数
arrSlope = []  # 用于存储每个像素的（X，Y）坐标
for i in range(nYSize):
    row = []
    for j in range(nXSize):
        px = adfGeoTransform[0] + i * adfGeoTransform[1] + j * adfGeoTransform[2]
        py = adfGeoTransform[3] + i * adfGeoTransform[4] + j * adfGeoTransform[5]
        col = [px, py]
        row.append(col)
    arrSlope.append(row)
#print(len(arrSlope))
#print(arrSlope)

import pandas as pd
arrSlope = pd.DataFrame(arrSlope)
#print(arrSlope[0])

