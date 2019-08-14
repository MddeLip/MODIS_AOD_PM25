# -*- coding: utf-8 -*-
# 时间    : 2019/1/31 11:12
# 作者    : xcl

from pyhdf.SD import SD
import os
import pandas as pd

output_file_path = "C:\\Users\\iii\\Desktop\\"
dir_str = "D:\\MODIS\\MCD19A2_1km_2015\\"
file_name = os.listdir(dir_str)
file_dir = [os.path.join(dir_str, x) for x in file_name]
#print(file_dir)
for hdf in file_dir:
    HDF_FILR_URL = hdf
    file = SD(HDF_FILR_URL)
    # print(file.info())
    datasets_dic = file.datasets()
    # 输出数据集名称
    for idx, sds in enumerate(datasets_dic.keys()):
        print(idx, sds)
    # 输出某项数据

    sds_obj = file.select('Injection_Height')  # 选择数据
    sds_obj = sds_obj.get()
    print(len(sds_obj[1]))
    #sds_obj = pd.DataFrame(sds_obj)
    #sds_obj.to_excel(output_file_path+"data.xlsx")
    # index输出
    # pd.DataFrame(datasets_dic.keys()).to_excel(output_file_path+"index.xlsx")
    # print(sds_obj[360][3], sds_obj.shape, sep="\n")
    break