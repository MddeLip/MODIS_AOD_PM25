# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/6 20:16

# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/6 16:59

# 库
import pandas as pd
import math
import numpy as np
import copy

# 路径
xytodis = pd.read_excel("C:\\Users\\iii\\Desktop\\xytodis.xlsx")
input_file_path_2 = "D:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Aqua\\2018\\北京-定陵.xlsx"
input_file_path_1 = "D:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Terra\\2018\\北京-定陵.xlsx"
# 读取
data1 = pd.read_excel(input_file_path_1)
data2 = pd.read_excel(input_file_path_2)

# 合并
if len(data1["日期"]) >= len(data2["日期"]):
    data3 = pd.merge(data1, data2, how='left', on=["日期", "监测站"])
else:
    data3 = pd.merge(data1, data2, how='right', on=["日期", "监测站"])

# 重设索引
data3 = data3.set_index('日期')
data2 = data2.set_index('日期')
data3.index = pd.to_datetime(data3.index)  # 转化为时间格式
del data2["监测站"]


'''
for name in data3.columns:
    for value in data3[name]:
        if pd.isnull(value):  # 判断是否为空
            print("控制")

        else:
            print(value)
'''
list_to_concat = []
for count in range(len(data2.index)):
    data_to_add = pd.DataFrame(list(data2.iloc[count]))  # 某一行
    data_to_dis = pd.concat([data_to_add, xytodis], axis=1)  # 坐标和某一行合并
    data_to_dis.columns = ["value", "index", "longitude", "latitude"]
    # 对这一行进行操作 对每一行输出一下
    for count_2 in range(len(data_to_dis["value"])):
        res_list = []
        if pd.isnull(data_to_dis.iloc[count_2]['value']):
            record = data_to_dis.iloc[count_2]['value']
            data_to_weight = data_to_dis[data_to_dis["value"] > 0]
            if len(data_to_weight["value"]) > 0:
                for item in range(len(data_to_weight["value"])):
                    dx = 1 * (data_to_weight.iloc[item]["longitude"] -
                              data_to_dis.iloc[count_2]['longitude'])
                    dy = 1 * (data_to_weight.iloc[item]["latitude"] -
                              data_to_dis.iloc[count_2]['latitude'])
                    weight = 1 / ((dx * dx + dy * dy) ** 0.5)
                    '''
                    if weight > 9999:
                        weight = np.nan
                    '''
                    res = weight * data_to_weight.iloc[item]["value"]
                    res_list.append(res)
                res_output = np.average(np.array(res_list))
                try:
                    data_to_dis.loc[count_2, 'value'] = res_output
                except Exception as e:
                    print("缺失严重, 插值未定义:", e)
    data_to_dis = data_to_dis.drop(["latitude", "longitude"], axis=1)
    data_to_dis = data_to_dis.drop(["index"], axis=1)
    list_to_concat.append(data_to_dis.T)
data_last = pd.concat(list_to_concat)

data_last.to_excel("data3.xlsx")
