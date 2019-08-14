# -*- coding: utf-8 -*-
# 时间    : 2019/1/22 20:50
# 作者    : xcl

'''
版本介绍:
1.适用于MODIS04_3KM文件
功能介绍:
1.检验是否存在无法打开的文件
2.删除
备注：
1.删除后,自行通过cmd进行批量下载
'''

# 相关库
from pyhdf.SD import SD, SDC  # 批量导入HDF
import os

# HDF文件位置
file_path = "D:\\MOD17_9-12\\"

# 批量读取
dir_str = file_path  # 文件位置
file_name = os.listdir(dir_str)  # 文件名
i = 0
error_file = []
print("共%s个文件" % len(file_name))
print("正在检索...")
for hdf in file_name:
    try:
        HDF_FILR_URL = file_path + hdf
        file = SD(HDF_FILR_URL)
        datasets_dic = file.datasets()
        i = i + 1  # 计数
        print("当前进度:" + str(format(i / len(file_name), ".00%")))
        # print(hdf+"第"+str(i)+"个文件完整")
    except Exception as e:
        i = i + 1
        # print(hdf+"第"+str(i)+"个文件错误")
        error_information = hdf + "第" + str(i) + "个文件错误"
        # error_file.append(error_information)
        error_file.append(hdf)


print("错误文件个数:" + str(len(error_file)) + "个")

'''
file=open('错误文件信息.txt','w')
file.write(str(error_file))
file.close()
'''

# 批量删除
for item in error_file:
    os.remove(file_path + item)
    print("已删除" + item)
