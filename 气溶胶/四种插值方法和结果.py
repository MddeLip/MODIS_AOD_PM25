# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 11:10


# 库
import pandas as pd
import numpy as np
from fancyimpute import KNN, IterativeImputer
import os
# 路径
input_file_path_Aqua = "D:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Aqua\\2018\\"
input_file_path_Terra = "D:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Terra\\2018\\"
merge_output_file_path = "D:\\毕业论文程序\\气溶胶光学厚度\\插值模块\\Merge\\2018\\"
mean_output_file_path = "D:\\毕业论文程序\\气溶胶光学厚度\\插值模块\\Mean\\2018\\"
xytodis = pd.read_excel("D:\\毕业论文程序\\气溶胶光学厚度\\插值模块\\xytodis.xlsx")  # 17个区域的投影坐标
input_file_names = os.listdir(input_file_path_Aqua)  # 文件名列表


# 空间局部公式: 不存在插值为1*nan=nan的插值结果;只存在nan*nan=nan -> 因为使用的插值数据已经筛选为'>0'的部分.
def get_IDW(input_data):
    list_to_concat = []
    for count in range(len(input_data.index)):
        data_to_add = pd.DataFrame(list(input_data.iloc[count]))  # 把某一行 转换成 列表 从而把行转化成 df中的列,不会修改原数据
        data_to_dis = pd.concat([data_to_add, xytodis], axis=1)  # 坐标和某一行合并
        # 这里使用简单合并的原因: 每行格式都是一致的,AOD0-16完美对应xytodis
        # print(data_to_dis, input_data.iloc[count], "================================", sep="\n")
        data_to_dis.columns = ["value", "index", "longitude", "latitude"]
        # 对这一行进行操作 对每一行输出一下
        for count_2 in range(len(data_to_dis["value"])):
            res_list = []
            weight_list = []
            if pd.isnull(data_to_dis.iloc[count_2]['value']):
                data_to_weight = data_to_dis[data_to_dis["value"] > 0]
                if len(data_to_weight["value"]) > 0:
                    # 先求权重
                    for item in range(len(data_to_weight["value"])):
                        dx = 1 * (data_to_weight.iloc[item]["longitude"] -
                                  data_to_dis.iloc[count_2]['longitude'])
                        dy = 1 * (data_to_weight.iloc[item]["latitude"] -
                                  data_to_dis.iloc[count_2]['latitude'])
                        weight_dis = 1 / ((dx * dx + dy * dy) ** 0.5)
                        # weight = inf ?
                        weight_list.append(weight_dis)
                    weight_sum = np.sum(np.array(weight_list))
                    # 计算结果
                    for item in range(len(data_to_weight["value"])):
                        dx = 1 * (data_to_weight.iloc[item]["longitude"] -
                                  data_to_dis.iloc[count_2]['longitude'])
                        dy = 1 * (data_to_weight.iloc[item]["latitude"] -
                                  data_to_dis.iloc[count_2]['latitude'])
                        weight_dis = 1 / ((dx * dx + dy * dy) ** 0.5)
                        res = (weight_dis/weight_sum) * data_to_weight.iloc[item]["value"]
                        res_list.append(res)
                    res_output = np.sum(np.array(res_list))  # 插补的数值
                    try:
                        data_to_dis.loc[count_2, 'value'] = res_output  # 进行插补
                    except Exception as e:
                        print("缺失严重, 插值未定义:", e)
        data_to_dis = data_to_dis.drop(["latitude", "longitude"], axis=1)   # 删除无用列
        data_to_dis = data_to_dis.drop(["index"], axis=1)
        list_to_concat.append(data_to_dis.T)  # 添加,行转化为列,合并中最终数据.
    data_last = pd.concat(list_to_concat)
    return data_last


for input_file_name in input_file_names:
    print("========正在计算%s========" % input_file_name)
    # 读取
    data_Aqua = pd.read_excel(input_file_path_Aqua + input_file_name)
    data_Terra = pd.read_excel(input_file_path_Terra + input_file_name)
    # 删除字符串,便于计算
    del data_Terra["监测站"]
    del data_Aqua["监测站"]
    data_Aqua = data_Aqua.set_index('日期')
    data_Terra = data_Terra.set_index('日期')
    # 时间局部：KNN
    # 最近邻估算，使用两行都具有观测数据的特征的均方差来对样本进行加权。然后用加权的结果进行特征值填充
    # 相当于A0D17个点为特征进行近邻,则参数K为时间,即时间上最近的16行按特征的均方差进行加权，即哪个时间点的权重大一些
    data_Aqua_KNN = KNN(k=7).fit_transform(data_Aqua)
    data_Aqua_KNN = pd.DataFrame(data_Aqua_KNN)  # 结果中有许多零值,应为空值
    data_Terra_KNN = KNN(k=7).fit_transform(data_Terra)
    data_Terra_KNN = pd.DataFrame(data_Terra_KNN)  # 结果中有许多零值,应为空值

    # 时间全局: 平滑,常用于股市
    data_Aqua_ewm = pd.DataFrame.ewm(
        self=data_Aqua,
        com=0.5,
        ignore_na=True,
        adjust=True).mean()
    data_Terra_ewm = pd.DataFrame.ewm(
        self=data_Terra,
        com=0.5,
        ignore_na=True,
        adjust=True).mean()

    # 空间局部: IDW
    data_Aqua_IDW = get_IDW(data_Aqua)
    data_Terra_IDW = get_IDW(data_Terra)

    # 空间全局: 迭代函数法,缺失特征作为y，其他特征作为x
    data_Aqua_Iterative = IterativeImputer(
        max_iter=10).fit_transform(data_Aqua)
    data_Aqua_Iterative = pd.DataFrame(data_Aqua_Iterative)
    data_Terra_Iterative = IterativeImputer(
        max_iter=10).fit_transform(data_Terra)
    data_Terra_Iterative = pd.DataFrame(data_Terra_Iterative)

    # 对结果的0值取np.nan
    data_Aqua_KNN.replace(0, np.nan, inplace=True)
    data_Terra_KNN.replace(0, np.nan, inplace=True)
    data_Aqua_ewm.replace(0, np.nan, inplace=True)
    data_Terra_ewm.replace(0, np.nan, inplace=True)
    data_Aqua_IDW.replace(0, np.nan, inplace=True)
    data_Terra_IDW.replace(0, np.nan, inplace=True)
    data_Aqua_Iterative.replace(0, np.nan, inplace=True)
    data_Terra_Iterative.replace(0, np.nan, inplace=True)

    # 合并相同方法的结果
    data_Aqua_KNN = data_Aqua_KNN.set_index(data_Aqua.index)
    data_Aqua_KNN.columns = data_Aqua.columns
    data_Aqua_KNN["日期合并用"] = data_Aqua_KNN.index
    data_Aqua_ewm = data_Aqua_ewm.set_index(data_Aqua.index)
    data_Aqua_ewm.columns = data_Aqua.columns
    data_Aqua_ewm["日期合并用"] = data_Aqua_ewm.index
    data_Aqua_IDW = data_Aqua_IDW.set_index(data_Aqua.index)
    data_Aqua_IDW.columns = data_Aqua.columns
    data_Aqua_IDW["日期合并用"] = data_Aqua_IDW.index
    data_Aqua_Iterative = data_Aqua_Iterative.set_index(data_Aqua.index)
    data_Aqua_Iterative.columns = data_Aqua.columns
    data_Aqua_Iterative["日期合并用"] = data_Aqua_Iterative.index

    data_Terra_KNN = data_Terra_KNN.set_index(data_Terra.index)
    data_Terra_KNN.columns = data_Terra.columns
    data_Terra_KNN["日期合并用"] = data_Terra_KNN.index
    data_Terra_ewm = data_Terra_ewm.set_index(data_Terra.index)
    data_Terra_ewm.columns = data_Terra.columns
    data_Terra_ewm["日期合并用"] = data_Terra_ewm.index
    data_Terra_IDW = data_Terra_IDW.set_index(data_Terra.index)
    data_Terra_IDW.columns = data_Terra.columns
    data_Terra_IDW["日期合并用"] = data_Terra_IDW.index
    data_Terra_Iterative = data_Terra_Iterative.set_index(data_Terra.index)
    data_Terra_Iterative.columns = data_Terra.columns
    data_Terra_Iterative["日期合并用"] = data_Terra_Iterative.index

    # 合并不同方法下的A/T为一个文件
    sheet_name = ["KNN", "ewm", "IDW", "Iterative"]
    sheet_name_count = 0  # 为什么显示without usage ?  因为下面如果if为false则..
    writer = pd.ExcelWriter(merge_output_file_path+'%s.xlsx' % (input_file_name.replace(".xlsx", "")))
    for methods_output in [[data_Aqua_KNN, data_Terra_KNN], [data_Aqua_ewm, data_Terra_ewm], [
            data_Aqua_IDW, data_Terra_IDW], [data_Aqua_Iterative, data_Terra_Iterative]]:
        if len(methods_output[0].index) >= len(methods_output[1].index):
            data_merge_AT = pd.merge(
                methods_output[0],
                methods_output[1],
                how='left',
                on=["日期"])
            data_merge_AT.to_excel(
                writer, sheet_name=sheet_name[sheet_name_count])
        else:
            data_merge_AT = pd.merge(
                methods_output[0],
                methods_output[1],
                how='right',
                on=["日期"])
            data_merge_AT.to_excel(
                writer, sheet_name=sheet_name[sheet_name_count])
        sheet_name_count = 1 + sheet_name_count
    writer.save()

    # AQ.mean(1) 对两颗卫星去均值, 列的横向均值
    writer = pd.ExcelWriter(mean_output_file_path+'%s.xlsx' % (input_file_name.replace(".xlsx", "")))
    for methods_output in sheet_name:
        data_to_mean = pd.read_excel(merge_output_file_path+'%s.xlsx' % (input_file_name.replace(".xlsx", "")), sheet_name=methods_output)
        data_to_mean = data_to_mean.set_index("日期")
        for area_numb in range(0, 17):
            d1 = data_to_mean[['AOD_%s_x' % area_numb, "AOD_%s_y" % area_numb]]
            d2 = d1.mean(1)
            data_to_mean["AOD_%s" % area_numb] = d2
            data_to_mean.drop(['AOD_%s_x' %
                               area_numb, "AOD_%s_y" %
                               area_numb], inplace=True, axis=1)
        data_to_mean.drop(['日期合并用_y', "日期合并用_x"], inplace=True, axis=1)
        data_to_mean.to_excel(writer, sheet_name=methods_output)
    writer.save()
