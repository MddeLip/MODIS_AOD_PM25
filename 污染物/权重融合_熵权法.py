# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 18:54

# 库
import pandas as pd
import numpy as np
import math
from numpy import array
import os

# 问题: 去掉空值后计算...权重大部分均为1/4; 如何改善?

# 定义熵值法函数
def cal_weight(x):
    # 标准化
    x = x.apply(lambda x: ((x - np.min(x)) / (np.max(x) - np.min(x))))

    # 求k
    rows = x.index.size  # 行
    cols = x.columns.size  # 列
    k = 1.0 / math.log(rows)

    lnf = [[None] * cols for i in range(rows)]

    # 矩阵计算--
    # 信息熵
    # p=array(p)
    x = array(x)
    lnf = [[None] * cols for i in range(rows)]
    lnf = array(lnf)
    for i in range(0, rows):
        for j in range(0, cols):
            if x[i][j] == 0:
                lnfij = 0.0
            else:
                p = x[i][j] / x.sum(axis=0)[j]
                lnfij = math.log(p) * p * (-k)
            lnf[i][j] = lnfij
    lnf = pd.DataFrame(lnf)
    E = lnf

    # 计算冗余度
    d = 1 - E.sum(axis=0)
    # 计算各指标的权重
    w = [[None] * 1 for i in range(cols)]
    for j in range(0, cols):
        wj = d[j] / sum(d)
        w[j] = wj
        # 计算各样本的综合得分,用最原始的数据

    w = pd.DataFrame(w)
    return w


Merge_output_file_path = "D:\\毕业论文程序\\污染物浓度\\插值模块\\Merge\\多年合一\\"
res_output_path = "D:\\毕业论文程序\\污染物浓度\\插值模块\\Res\\多年合一\\"

input_file_names = os.listdir(Merge_output_file_path)  # 文件名列表
for input_file_name in input_file_names:
    # 读取
    data_KNN = pd.read_excel(
        Merge_output_file_path +
        input_file_name,
        sheet_name="KNN")
    data_ewm = pd.read_excel(
        Merge_output_file_path +
        input_file_name,
        sheet_name="ewm")
    data_IDW = pd.read_excel(
        Merge_output_file_path +
        input_file_name,
        sheet_name="IDW")
    data_Iterative = pd.read_excel(
        Merge_output_file_path +
        input_file_name,
        sheet_name="Iterative")
    # 结果列表
    res = []
    # for area_numb in range(0, 17):  # 这里需要修改
    for column_name in ["PM25", "PM10", "SO2", "NO2", "O3", "CO"]:
        d1 = data_KNN[["日期", column_name]]
        d2 = data_ewm[["日期", column_name]]
        data_Time = pd.merge(d1,
                             d2,
                             how='left',
                             on=["日期"])

        d3 = data_IDW[["日期", column_name]]
        d4 = data_Iterative[["日期", column_name]]
        data_Station = pd.merge(
            d3,
            d4,
            how='left',
            on=["日期"])

        data_aod = pd.merge(
            data_Time,
            data_Station,
            how='left',
            on=["日期"])
        data_aod.columns = ["日期", "KNN", "ewm", "IDW", "Iterative"]
        # data_aod.columns : 日期 AOD_0_x_x AOD_0_y_x AOD_0_x_y AOD_0_y_y
        data_aod = data_aod.set_index("日期")
        data_aod_to_weight = data_aod.dropna()  # 用非空值计算更合理
        w = cal_weight(data_aod_to_weight)  # 调用cal_weight
        w.index = data_aod.columns
        w.columns = ['weight']
        print(w)
        '''
        value_weight= data_aod["KNN"] * w.weight[0] + data_aod["ewm"] * \
            w.weight[1] + data_aod["IDW"] * w.weight[2] + data_aod["Iterative"] * w.weight[3]
        # print(data_aod.isnull().sum())
        '''
        value_weight_list = []
        for loc in range(len(data_aod.index)):
            # 四种方法均不缺失
            if pd.notnull(
                data_aod["KNN"][loc]) and pd.notnull(
                data_aod["ewm"][loc]) and pd.notnull(
                data_aod["IDW"][loc]) and pd.notnull(
                    data_aod["Iterative"][loc]):
                value_weight = data_aod["KNN"][loc] * w.weight[0] + data_aod["ewm"][loc] * w.weight[1] +\
                    data_aod["IDW"][loc] * w.weight[2] + data_aod["Iterative"][loc] * w.weight[3]
            # 某一种缺失
            elif pd.isnull(data_aod["KNN"][loc]) and pd.notnull(data_aod["ewm"][loc]) and pd.notnull(data_aod["IDW"][loc]) and \
                    pd.notnull(data_aod["Iterative"][loc]):
                value_weight = data_aod["ewm"][loc] * (w.weight[1] / (w.weight[1] + w.weight[2] + w.weight[3])) + \
                    data_aod["IDW"][loc] * (w.weight[2] / (w.weight[1] + w.weight[2] + w.weight[3])) +\
                    data_aod["Iterative"][loc] * (w.weight[3] / (w.weight[1] + w.weight[2] + w.weight[3]))
            elif pd.notnull(data_aod["KNN"][loc]) and pd.isnull(data_aod["ewm"][loc]) and pd.notnull(data_aod["IDW"][loc]) and \
                    pd.notnull(data_aod["Iterative"][loc]):
                value_weight = data_aod["KNN"][loc] * (w.weight[0] / (w.weight[0] + w.weight[2] + w.weight[3])) +\
                    data_aod["IDW"][loc] * (w.weight[2] / (w.weight[0] + w.weight[2] + w.weight[3])) +\
                    data_aod["Iterative"][loc] * (w.weight[3] / (w.weight[0] + w.weight[2] + w.weight[3]))
            elif pd.notnull(data_aod["KNN"][loc]) and pd.notnull(data_aod["ewm"][loc]) and pd.isnull(data_aod["IDW"][loc]) and \
                    pd.notnull(data_aod["Iterative"][loc]):
                value_weight = data_aod["KNN"][loc] * (
                    w.weight[0] / (w.weight[0] + w.weight[1] + w.weight[3])) + \
                    data_aod["ewm"][loc] * (
                    w.weight[1] / (w.weight[0] + w.weight[1] + w.weight[3])) + \
                    data_aod["Iterative"][loc] * (
                    w.weight[3] / (w.weight[0] + w.weight[1] + w.weight[3]))
            elif pd.notnull(data_aod["KNN"][loc]) and pd.notnull(data_aod["ewm"][loc]) and pd.notnull(data_aod["IDW"][loc]) and \
                    pd.isnull(data_aod["Iterative"][loc]):
                value_weight = data_aod["KNN"][loc] * (
                    w.weight[0] / (w.weight[0] + w.weight[1] + w.weight[2])) + \
                    data_aod["ewm"][loc] * (
                    w.weight[1] / (w.weight[0] + w.weight[1] + w.weight[2])) + \
                    data_aod["IDW"][loc] * (
                    w.weight[2] / (w.weight[0] + w.weight[1] + w.weight[2]))
            # 两种缺失
            elif pd.isnull(data_aod["KNN"][loc]) and pd.isnull(data_aod["ewm"][loc]) and pd.notnull(data_aod["IDW"][loc]) and \
                    pd.notnull(data_aod["Iterative"][loc]):
                value_weight = data_aod["IDW"][loc] * (w.weight[2] / (w.weight[2] + w.weight[3])) + \
                    data_aod["Iterative"][loc] * (w.weight[3] / (w.weight[2] + w.weight[3]))
            elif pd.isnull(data_aod["KNN"][loc]) and pd.notnull(data_aod["ewm"][loc]) and pd.isnull(data_aod["IDW"][loc]) and \
                    pd.notnull(data_aod["Iterative"][loc]):
                value_weight = data_aod["ewm"][loc] * (w.weight[1] / (w.weight[1] + w.weight[3])) + \
                    data_aod["Iterative"][loc] * (w.weight[3] / (w.weight[1] + w.weight[3]))
            elif pd.isnull(data_aod["KNN"][loc]) and pd.notnull(data_aod["ewm"][loc]) and pd.notnull(data_aod["IDW"][loc]) and \
                    pd.isnull(data_aod["Iterative"][loc]):
                value_weight = data_aod["ewm"][loc] * (w.weight[1] / (w.weight[1] + w.weight[2])) + \
                    data_aod["IDW"][loc] * (w.weight[2] / (w.weight[1] + w.weight[2]))
            elif pd.notnull(data_aod["KNN"][loc]) and pd.isnull(data_aod["ewm"][loc]) and pd.isnull(data_aod["IDW"][loc]) and \
                    pd.notnull(data_aod["Iterative"][loc]):
                value_weight = data_aod["KNN"][loc] * (w.weight[0] / (w.weight[0] + w.weight[3])) + \
                    data_aod["Iterative"][loc] * (w.weight[3] / (w.weight[0] + w.weight[3]))
            elif pd.notnull(data_aod["KNN"][loc]) and pd.isnull(data_aod["ewm"][loc]) and pd.notnull(data_aod["IDW"][loc]) and \
                    pd.isnull(data_aod["Iterative"][loc]):
                value_weight = data_aod["KNN"][loc] * (w.weight[0] / (w.weight[0] + w.weight[2])) + \
                    data_aod["IDW"][loc] * (w.weight[2] / (w.weight[0] + w.weight[2]))
            elif pd.notnull(data_aod["KNN"][loc]) and pd.notnull(data_aod["ewm"][loc]) and pd.isnull(data_aod["IDW"][loc]) and \
                    pd.isnull(data_aod["Iterative"][loc]):
                value_weight = data_aod["KNN"][loc] * (w.weight[0] / (w.weight[0] + w.weight[1])) + \
                    data_aod["IDW"][loc] * (w.weight[1] / (w.weight[0] + w.weight[1]))
            # 三种缺失
            elif pd.notnull(data_aod["KNN"][loc]) and pd.isnull(data_aod["ewm"][loc]) and pd.isnull(data_aod["IDW"][loc]) and \
                    pd.isnull(data_aod["Iterative"][loc]):
                value_weight = data_aod["KNN"][loc] * w.weight[0]
            elif pd.isnull(data_aod["KNN"][loc]) and pd.notnull(data_aod["ewm"][loc]) and pd.isnull(data_aod["IDW"][loc]) and \
                    pd.isnull(data_aod["Iterative"][loc]):
                value_weight = data_aod["ewm"][loc] * w.weight[1]
            elif pd.isnull(data_aod["KNN"][loc]) and pd.isnull(data_aod["ewm"][loc]) and pd.notnull(data_aod["IDW"][loc]) and \
                    pd.isnull(data_aod["Iterative"][loc]):
                value_weight = data_aod["IDW"][loc] * w.weight[2]
            elif pd.isnull(data_aod["KNN"][loc]) and pd.isnull(data_aod["ewm"][loc]) and pd.isnull(data_aod["IDW"][loc]) and \
                    pd.notnull(data_aod["Iterative"][loc]):
                value_weight = data_aod["Iterative"][loc] * w.weight[3]
            else:
                value_weight = -9999
            value_weight_list.append(value_weight)
            # print(value_weight)
        value_weight_list = pd.DataFrame(value_weight_list)
        value_weight_list = value_weight_list.set_index(data_aod.index)
        value_weight_list.columns = [column_name]
        connect_data = pd.merge(
            data_aod,
            value_weight_list,
            left_index=True,
            right_index=True)
        connect_data = connect_data.drop(
            columns=["KNN", "ewm", "IDW", "Iterative"])
        res.append(connect_data)

    res_data = pd.concat(res, sort=False, axis=1)
    res_data.to_excel(res_output_path + input_file_name)
    print("已输出:" + "%s" % input_file_name)
