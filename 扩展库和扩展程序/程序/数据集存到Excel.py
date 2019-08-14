# -*- coding: utf-8 -*-
# 时间    : 2019/2/1 19:31
# 作者    : xcl


import warnings
import pandas as pd  # BDS
from pyhdf.SD import SD  # 批量导入HDF
import datetime  # 程序耗时
import os  # 关机,批量文件
import time  # 关机

# 忽视空列表计算均值而导致的警告
warnings.filterwarnings('ignore')

# 开始计算耗时
start_time = datetime.datetime.now()


# 参数设置
r = 7500   # 参照文献;经纬度转换为的距离范围,监测站3KM半径范围内为观测区域
file_path = "F:\\MODIS\\modis04_3km_A\\"  # HDF文件位置
output_file_path = "C:\\Users\\寻常鹿\\Desktop\\Excel数据集\\"  # 结果的输出位置


# 批量读取HDF文件,提取AOD值,并将结果添加到列表中
file_name = os.listdir(file_path)  # 文件名

i = 0
for hdf in file_name:
    i = i + 1
    HDF_FILE_URL = file_path + hdf
    file = SD(HDF_FILE_URL)
    data_sets_dic = file.datasets()
    '''
    #输出数据集名称
    for idx, sds in enumerate(data_sets_dic.keys()):
       print(idx, sds)
    '''
    sds_obj1 = file.select('Longitude')  # 选择经度
    sds_obj2 = file.select('Latitude')  # 选择纬度
    sds_obj3 = file.select('Optical_Depth_Land_And_Ocean')  # 产品质量最高的AOD数据集
    longitude = sds_obj1.get()  # 读取数据
    latitude = sds_obj2.get()
    aod = sds_obj3.get()
    writer = pd.ExcelWriter(output_file_path + '%s.xlsx' % hdf)

    longitude = pd.DataFrame(longitude)  # 格式转换
    latitude = pd.DataFrame(latitude)
    aod = pd.DataFrame(aod)

    longitude.to_excel(writer, sheet_name='longitude')
    latitude.to_excel(writer, sheet_name='latitude')
    aod.to_excel(writer, sheet_name='aod')
    writer.close()
    print("进度:%.2f%%" % (100*i/len(file_name)))


# 程序运行完成后关机
def shutdown_computer(seconds):
    print("程序已完成," + str(seconds) + '秒后将会关机')
    time.sleep(seconds)
    print('关机')
    os.system('shutdown -s -f -t 1')


# shutdown_computer(60)
