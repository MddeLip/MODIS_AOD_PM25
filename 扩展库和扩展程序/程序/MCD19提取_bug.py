# -*- coding: utf-8 -*-
# 时间    : 2019/1/22 20:50
# 作者    : xcl
import pandas as pd
import numpy as np
import h5py  # 导入工具包
import numpy as np


from pyhdf.SD import SD, SDC #批量导入HDF
import os

# HDF文件位置
file_path = "D:\\MODIS\\MCD19A2_1km_2015\\"
file = file_path+"MCD19A2.A2015023.h23v05.006.2018101234406.hdf"
file = file_path+"MCD19A2.A2015001.h28v05.006.2018101210327.hdf"

#file = file_path+"MCD19A1.A2018334.h33v10.006.2018336034517.hdf"
#print(file_dir)


file = SD(file)
#print(file.info())
datasets_dic = file.datasets()
#print(file.datasets())

data1 = file.select('Optical_Depth_047')
print(data1.get().shape)
#print(data1.get().head())
attributes = data1.attributes()
print(attributes)
data1np = data1.get()


print(data1np[0])

data1np = np.array(data1np[0])
data1np = pd.DataFrame(data1np)
print(data1np)
#data1np = pd.DataFrame(data1np)

data1np.to_excel("test1.xlsx")






#data2 = file.select('Optical_Depth_055')

#c = data1.get()
#print(c.shape)

#d = data1.attributes()
#print(d)