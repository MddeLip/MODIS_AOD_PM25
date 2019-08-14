# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/9 1:10

'''
说明:
    v4 分年份输出
    v5 多年份合一,省去拼接
'''

# 相关库
import time
import os
import pandas as pd
import warnings
from datetime import datetime as dt
import datetime

# 第一部分
# 参数设置
'''
path_list = ["D:\\站点_20140513-20141231\\",
             "D:\\站点_20150101-20151231\\",
             "D:\\站点_20160101-20161231\\",
             "D:\\站点_20170101-20171231\\",
             "D:\\站点_20180101-20181231\\"]
'''

path_list = ["D:\\站点14-18\\"]


# 文件夹循环
for path in path_list:
    input_file_path = path
    input_file_name = os.listdir(input_file_path)  # 文件名
    output_file_path = "D:\\毕业论文程序\\污染物浓度\\污染物数据\\日均\\total\\"
    error_path = "D:\\毕业论文程序\\污染物浓度\\error\\"
    JCZ_data = pd.read_excel(
        "D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx",
        sheet_name="汇总")
    # JCZ_data = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx",
    # sheet_name="北京2019")  # 适用于北京2019年
    JCZ_number = JCZ_data["监测点编码"]

    # 主程序, 主要部分
    i = 0
    for number in JCZ_number:
        i += 1
        print("当前进度:%.2f%%" % (i / (len(JCZ_number)*len(path_list)) * 100))
        error = []
        outcome_list_PM25 = []
        outcome_list_PM10 = []
        outcome_list_SO2 = []
        outcome_list_NO2 = []
        outcome_list_O3 = []
        outcome_list_CO = []
        # print(number)
        for file in input_file_name:
            # print(file)
            date = file.replace("china_sites_", "").replace(".csv", "")  # 中国站点
            # date = file.replace("beijing_all_", "").replace(".csv", "")  #  北京
            # date = file.replace("china_cities_", "").replace(".csv", "")  # 中国城市
            # 日期格式: 使用文件名更改
            date = time.strptime(date, '%Y%m%d')
            date = time.strftime("%Y-%m-%d", date)
            date = dt.strptime(date, '%Y-%m-%d').date()
            try:
                data = pd.read_csv(input_file_path + file, encoding='utf8')
                data = data[data["type"].isin(
                    ['PM10_24h', 'SO2_24h', "NO2_24h", "O3_24h", "CO_24h", "PM2.5_24h"])]
                data = data[data["hour"] == 0]
                # 为合并做准备

                # 筛选行: 返回 同类型污染物的多个监测站数据
                data_PM25 = data[data["type"] == "PM2.5_24h"]
                data_PM10 = data[data["type"] == "PM10_24h"]
                data_SO2 = data[data["type"] == "SO2_24h"]
                data_NO2 = data[data["type"] == "NO2_24h"]
                data_O3 = data[data["type"] == "O3_24h"]
                data_CO = data[data["type"] == "CO_24h"]

                # 今日0时的24小时平均滑动值是前一天的24小时PM2.5均值
                # print(file)
                '''
                先对同一个type合并在一起。
                再合并不同的污染物
                '''
                # 筛选列: 返回 同污染物 同监测站
                # 原版代码: [["hour", "%s" % number]]
                data_PM25 = data_PM25[["%s" % number]]
                data_PM10 = data_PM10[["%s" % number]]
                data_SO2 = data_SO2[["%s" % number]]
                data_NO2 = data_NO2[["%s" % number]]
                data_O3 = data_O3[["%s" % number]]
                data_CO = data_CO[["%s" % number]]
                # 设置日期
                data_PM25["日期"] = date
                data_PM10["日期"] = date
                data_NO2["日期"] = date
                data_SO2["日期"] = date
                data_O3["日期"] = date
                data_CO["日期"] = date

                # 添加进列表
                outcome_list_PM25.append(data_PM25)
                outcome_list_PM10.append(data_PM10)
                outcome_list_NO2.append(data_NO2)
                outcome_list_SO2.append(data_SO2)
                outcome_list_O3.append(data_O3)
                outcome_list_CO.append(data_CO)
                # print(file, "正常")
            except Exception as e:
                print(file, "报错:", e)
                problem = file, e
                error.append(problem)
        outcome_PM25 = pd.concat(outcome_list_PM25)
        outcome_PM10 = pd.concat(outcome_list_PM10)
        outcome_SO2 = pd.concat(outcome_list_SO2)
        outcome_NO2 = pd.concat(outcome_list_NO2)
        outcome_O3 = pd.concat(outcome_list_O3)
        outcome_CO = pd.concat(outcome_list_CO)

        # 修改列名
        outcome_PM25.rename(columns={"%s" % number: 'PM25'}, inplace=True)
        outcome_PM10.rename(columns={"%s" % number: 'PM10'}, inplace=True)
        outcome_SO2.rename(columns={"%s" % number: 'SO2'}, inplace=True)
        outcome_NO2.rename(columns={"%s" % number: 'NO2'}, inplace=True)
        outcome_O3.rename(columns={"%s" % number: 'O3'}, inplace=True)
        outcome_CO.rename(columns={"%s" % number: 'CO'}, inplace=True)

        # 排序
        outcome_PM25 = outcome_PM25.sort_values("日期", ascending=True)
        outcome_PM10 = outcome_PM10.sort_values("日期", ascending=True)
        outcome_NO2 = outcome_NO2.sort_values("日期", ascending=True)
        outcome_SO2 = outcome_SO2.sort_values("日期", ascending=True)
        outcome_O3 = outcome_O3.sort_values("日期", ascending=True)
        outcome_CO = outcome_CO.sort_values("日期", ascending=True)

        # 判断
        if len(outcome_PM25["日期"]) > len(outcome_PM10["日期"]):
            outcome = pd.merge(
                left=outcome_PM25,
                right=outcome_PM10,
                how="left",
                on="日期")
        else:
            outcome = pd.merge(
                left=outcome_PM25,
                right=outcome_PM10,
                how="right",
                on="日期")

        if len(outcome["日期"]) > len(outcome_SO2["日期"]):
            outcome = pd.merge(
                left=outcome,
                right=outcome_SO2,
                how="left",
                on="日期")
        else:
            outcome = pd.merge(
                left=outcome,
                right=outcome_SO2,
                how="right",
                on="日期")

        if len(outcome["日期"]) > len(outcome_NO2["日期"]):
            outcome = pd.merge(
                left=outcome,
                right=outcome_NO2,
                how="left",
                on="日期")
        else:
            outcome = pd.merge(
                left=outcome,
                right=outcome_NO2,
                how="right",
                on="日期")

        if len(outcome["日期"]) > len(outcome_O3["日期"]):
            outcome = pd.merge(
                left=outcome,
                right=outcome_O3,
                how="left",
                on="日期")
        else:
            outcome = pd.merge(
                left=outcome,
                right=outcome_O3,
                how="right",
                on="日期")

        if len(outcome["日期"]) > len(outcome_CO["日期"]):
            outcome = pd.merge(
                left=outcome,
                right=outcome_CO,
                how="left",
                on="日期")
        else:
            outcome = pd.merge(
                left=outcome,
                right=outcome_CO,
                how="right",
                on="日期")

        # 重设索引
        outcome = outcome.set_index("日期")
        # 输出
        outcome.to_excel(output_file_path + "%s污染物浓度.xlsx" % number)
        pd.DataFrame(error).to_excel(error_path + "error.xlsx")


print("================ 开始第二部分 ==================")
# 第二部分: 更改日期为T-1, 增加站点名称列

warnings.filterwarnings('ignore')  # 代码中仅进行新列的赋值,不对数据源做修改,因此可以忽略该警告
# 参数设置
input_file_path = "D:\\毕业论文程序\\污染物浓度\\污染物数据\\日均\\total\\"
input_file_name = os.listdir(input_file_path)  # 文件名
output_file_path = "D:\\毕业论文程序\\污染物浓度\\整理\\全部污染物\\多年合一\\"
JCZ_NAME = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx", sheet_name="汇总")
# JCZ_NAME = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx", sheet_name="北京2019")  # 适用于北京2019年
# JCZ_NAME格式为df,监测站编码,监测点名称,城市,经度,纬度
# print(input_file_name)
# print(JCZ_NAME.head())

i = -1
for JCZ in input_file_name:
    i += 1
    print("进度:%.2f%%" % (i/(len(input_file_name)-1)*100))
    # print(JCZ)
    JCZ = JCZ.replace("污染物浓度.xlsx", "")
    # 获取对应监测点编码的名称和坐标信息
    JCZ_info = JCZ_NAME[JCZ_NAME["监测点编码"] == JCZ]
    # 为统一数据保存命名方式为"城市-监测站名称"
    JCZ_new_name = JCZ_info["城市"]+"-"+JCZ_info["监测点名称"]
    # JCZ_new_name = pd.DataFrame(JCZ_new_name)
    JCZ_new_name = JCZ_new_name.values[0]
    # print(JCZ_new_name.values)
    # print(JCZ_info.__class__)

    # 读取数据
    data = pd.read_excel(input_file_path+JCZ+"污染物浓度.xlsx")
    data["日期"] = data["日期"].dt.date
    '''
          今日0时的24小时平均滑动值是前一天的24小时PM2.5均值
    '''

    def get_day(date_input, step=0):  # step 默认为0
        # 获取指定日期date(形如"xxxx-xx-xx")之前或之后的多少天的日期, 返回值为字符串格式的日期
        date_input = str(date_input)  # 转化为字符串方便合并
        l_input = date_input.split("-")
        y = int(l_input[0])
        m = int(l_input[1])
        d = int(l_input[2])
        old_date = datetime.datetime(y, m, d)
        new_date = (old_date + datetime.timedelta(days=step)).strftime('%Y-%m-%d')
        # print(new_date)
        return new_date


    data["日期"] = data["日期"].map(lambda x: get_day(x, -1))  # 今日的0时PM2.5_24h对应前一天PM2.5日均值
    '''
    data["X"] = JCZ_info["经度"][i]
    data["Y"] = JCZ_info["纬度"][i]
    '''
    # 以下仅在北京2019年下使用
    '''
    data["X"] = JCZ_info["经度"]
    data["Y"] = JCZ_info["纬度"]
    data['X'] = data['X'].fillna(method='pad')
    data['Y'] = data['Y'].fillna(method='pad')  # 用前一个值补充坐标
    '''
    # 输出
    data = data.set_index('日期')
    data.to_excel(output_file_path + "%s.xlsx" % JCZ_new_name)
