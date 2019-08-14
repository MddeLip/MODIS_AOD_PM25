# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/7/15 13:02

# 库
from multiprocessing import Process  # 多线程,提高CPU利用率
import warnings
from math import radians, cos, sin, asin, sqrt, degrees, atan2  # 经纬度计算距离
import pandas as pd  # BDS
import numpy as np  # BDS
from pyhdf.SD import SD  # 批量导入HDF
import datetime  # 程序耗时
import os  # 关机,批量文件
import time  # 关机
from numba import jit

warnings.filterwarnings('ignore')  # 忽略"number/0"的情况
start_time = datetime.datetime.now()  # 耗时计算
# 参数设置
dis1 = 8000  # 同心圆范围
dis2 = 20000
dis3 = 50000

# 文件设置
output_file_path = "D:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Terra\\2018\\"  # 结果的输出位置
MODIS_input_file_path = "E:\\MOD04_3K_2018\\"  # HDF文件位置 TTT
location_xy_input_file = "D:\\毕业论文程序\\MODIS\\坐标\\站点列表-2018.11.08起.xlsx"
exist_file_list = os.listdir(output_file_path)
# 定义经纬度距离公式
@jit
def geo_distance(lng1, lat1, lng2, lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    d_lon = lng2 - lng1
    d_lat = lat2 - lat1
    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    dis = 2 * asin(sqrt(a)) * 6371.393 * 1000  # 地球半径
    return dis  # 输出结果的单位为“米”


# 计算方位角函数: 后输入位置在前输入位置的方位角
@jit
def getDegree(latA, lonA, latB, lonB):
    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)
    dLon = radLonB - radLonA
    y = sin(dLon) * cos(radLatB)
    x = cos(radLatA) * sin(radLatB) - sin(radLatA) * cos(radLatB) * cos(dLon)
    brng = degrees(atan2(y, x))
    brng = (brng + 360) % 360
    return brng


@jit(nogil=True)
# 此次,numpy切片的检索顺序是先"行"后"列"
def get_aod_list(longitude_df, latitude_df, aod_df, item_df1, item_df2):  # hdf经纬度, aod; 目标检测站经纬度
    a0_list = []
    a1_list = []
    a2_list = []
    a3_list = []
    a4_list = []
    a5_list = []
    a6_list = []
    a7_list = []
    a8_list = []
    b1_list = []
    b2_list = []
    b3_list = []
    b4_list = []
    b5_list = []
    b6_list = []
    b7_list = []
    b8_list = []
    for row in range(longitude_df.shape[0]):  # 行 676
        for column in range(longitude_df.shape[1]):  # 列 451
            # 超过50KM的数值记为缺失-9999
            if item_df1 - 0.8 <= longitude_df[row][column] <= item_df1 + 0.8 and \
                    item_df2 - 0.5 <= latitude_df[row][column] <= item_df2 + 0.5:
                # 获取经纬度之间的距离
                d = geo_distance(
                    longitude_df[row][column],
                    latitude_df[row][column],
                    item_df1,
                    item_df2)  # item[0],item[1]
            else:
                d = -9999  # 表示缺失
            # 根据距离和经纬度分为到不同列表
            if (d > 0) and (d <= dis1) and aod_df[row][column] > 0:  # 第1个圆,自身
                a0_list.append(aod_df[row][column])  # 第1个列表
            # 第2个圆,近邻
            elif (d > dis1) and (d <= dis2) and aod_df[row][column] > 0:
                # 角度公式返回值: 后面输入的经纬度位置在前面输入的经纬度位置的方位
                angle_res = getDegree(
                    item_df1,
                    item_df2,
                    longitude_df[row][column],
                    latitude_df[row][column])
                if 0 <= angle_res < 45:
                    a1_list.append(aod_df[row][column])
                elif 45 <= angle_res < 90:
                    a2_list.append(aod_df[row][column])
                elif 90 <= angle_res < 135:
                    a3_list.append(aod_df[row][column])
                elif 135 <= angle_res < 180:
                    a4_list.append(aod_df[row][column])
                elif 180 <= angle_res < 225:
                    a5_list.append(aod_df[row][column])
                elif 225 <= angle_res < 270:
                    a6_list.append(aod_df[row][column])
                elif 270 <= angle_res < 315:
                    a7_list.append(aod_df[row][column])
                else:
                    a8_list.append(aod_df[row][column])
            # 第3个圆,远邻
            elif (d > dis2) and (d <= dis3) and aod_df[row][column] > 0:
                angle_res = getDegree(
                    longitude_df[row][column],
                    latitude_df[row][column],
                    item_df1,
                    item_df2)
                if 0 <= angle_res < 45:
                    b1_list.append(aod_df[row][column])
                elif 45 <= angle_res < 90:
                    b2_list.append(aod_df[row][column])
                elif 90 <= angle_res < 135:
                    b3_list.append(aod_df[row][column])
                elif 135 <= angle_res < 180:
                    b4_list.append(aod_df[row][column])
                elif 180 <= angle_res < 225:
                    b5_list.append(aod_df[row][column])
                elif 225 <= angle_res < 270:
                    b6_list.append(aod_df[row][column])
                elif 270 <= angle_res < 315:
                    b7_list.append(aod_df[row][column])
                else:
                    b8_list.append(aod_df[row][column])
    return a0_list, a1_list, a2_list, a3_list, a4_list, a5_list, a6_list, a7_list, a8_list, b1_list, b2_list, b3_list, b4_list, b5_list, b6_list, b7_list, b8_list


file_name = os.listdir(MODIS_input_file_path)  # 批量读取HDF文件,提取AOD值,并将结果添加到列表中


def get_aod_multiprocessing(location_xy):
    JCZ_file = pd.read_excel(
        location_xy_input_file,
        sheet_name=location_xy)
    JCZ = []
    # 批量导入监测站
    for i in range(len(JCZ_file)):
        exec(
            'JCZ%s = [JCZ_file["经度"][i],JCZ_file["纬度"][i],JCZ_file["城市"][i]+"-"+JCZ_file["监测点名称"][i]]' %
            i)
        exec("JCZ.append(JCZ%s)" % i)  # exec可以执行字符串指令
    for item in JCZ:
        if item[2] + ".xlsx" in exist_file_list:    # 已输出文件不在重复计算
            print("文件已经存在")
            continue
        aod_outcome_list = []  # 每个监测站生成一个文件时
        for hdf in file_name:
            HDF_FILE_URL = MODIS_input_file_path + hdf
            file = SD(HDF_FILE_URL)
            sds_obj1 = file.select('Longitude')  # 选择经度
            sds_obj2 = file.select('Latitude')  # 选择纬度
            sds_obj3 = file.select(
                'Optical_Depth_Land_And_Ocean')  # 产品质量最高的AOD数据集
            longitude = sds_obj1.get()  # 读取数据
            latitude = sds_obj2.get()
            aod = sds_obj3.get()
            # 经度加±0.1，纬度加±0.075，这样7.5KM圈的范围也包含对了，避免出现四分之三元在文件内，四分之一不在二忽略文件
            if np.min(longitude) - 0.8 <= item[0] <= np.max(longitude) + 0.8 and \
                    np.min(latitude) - 0.5 <= item[1] <= np.max(latitude) + 0.5:
                # 距离计算，提取监测站半径为r范围内的AOD值!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                aod_list = get_aod_list(
                    longitude,
                    latitude,
                    aod,
                    item[0],
                    item[1])  # 内含一个文件的17个列表
                # 把返回的列表值取均值
                list_value = "%s文件" % hdf, "%s" % item[2], np.average(aod_list[0]), np.average(aod_list[1]), \
                    np.average(aod_list[2]), np.average(aod_list[3]), np.average(aod_list[4]), \
                    np.average(aod_list[5]), np.average(aod_list[6]), np.average(aod_list[7]), \
                    np.average(aod_list[8]), np.average(aod_list[9]), np.average(aod_list[10]), \
                    np.average(aod_list[11]), np.average(aod_list[12]), np.average(aod_list[13]), \
                    np.average(aod_list[14]), np.average(aod_list[15]), np.average(aod_list[16])
                # 添加进列表
                aod_outcome_list.append(list_value)
                # 进度提示
                print("完成 %s文件" % hdf, "%s" % item[2])
            else:
                print("不在 %s文件中: %s站点" % (hdf, item[2]))
        # 上一个for循环结束
        aod_outcome_list_result = []
        for element in aod_outcome_list:
            element = pd.Series(element)  # 格式转换
            # 截取文件名称,结果为获取数据的时间,格式为"年+第几天"
            element[0] = str(element[0])[10:17]  # 如2018123
            # 修改日期格式为XX月XX日
            element[0] = time.strptime(element[0], '%Y%j')
            element[0] = time.strftime("%Y-%m-%d ", element[0])
            element = np.array(element)  # 格式转换
            aod_outcome_list_result.append(element)
        # 避免输出结果字符串省略，四行设置都需要
        pd.set_option('display.max_rows', None)  # 行
        pd.set_option('display.max_columns', 1000)  # 列
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', 1000)
        aod_outcome_list_result = pd.DataFrame(aod_outcome_list_result)  # 格式转换
        # 重设列名
        aod_outcome_list_result.columns = [
            '日期',
            '监测站',
            "AOD_0",
            "AOD_1",
            "AOD_2",
            "AOD_3",
            "AOD_4",
            "AOD_5",
            "AOD_6",
            "AOD_7",
            "AOD_8",
            "AOD_9",
            "AOD_10",
            "AOD_11",
            "AOD_12",
            "AOD_13",
            "AOD_14",
            "AOD_15",
            "AOD_16"]
        # 同日期，多文件情况下的均值处理
        aod_outcome_list_result = aod_outcome_list_result.groupby(
            ['日期', "监测站"]).mean()
        # 美化group by均值计算后的数据框格式
        # aod_outcome_list_result = pd.Series(aod_outcome_list_result["AOD值"])  #
        # AOD值按分组计算的结果
        aod_outcome_list_result.to_excel(
            output_file_path + "%s.xlsx" %
            item[2])  # 完整结果存入excel

    # 程序用时写入文件
    end_time = datetime.datetime.now()
    print(str(end_time - start_time))


if __name__ == '__main__':
    print('=====主进程=====')
    print("总文件个数:", len(file_name))

    p1 = Process(target=get_aod_multiprocessing, args=('样例1',))
    p2 = Process(target=get_aod_multiprocessing, args=('样例2',))
    p3 = Process(target=get_aod_multiprocessing, args=('样例3',))
    p4 = Process(target=get_aod_multiprocessing, args=('样例4',))
    p5 = Process(target=get_aod_multiprocessing, args=('样例5',))
    p6 = Process(target=get_aod_multiprocessing, args=('样例6',))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()

    p6.join()  # 依次检测是否完成, 完成才会执行join下面的代码
    p5.join()
    p4.join()
    p3.join()
    p2.join()
    p1.join()

    # 自动关机
    print("程序已完成," + str(60) + '秒后将会关机')
    time.sleep(60)
    print('关机')
    os.system('shutdown -s -f -t 1')
