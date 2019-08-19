# -*- coding: utf-8 -*-
# 日期: 2019/5/11 11:17
# 作者: xcl
# 工具：PyCharm

from darksky import forecast  # DarkSkyAPI
import time  # 年度时间范围生成
from datetime import datetime as dt  # 时间戳日期转换
import pandas as pd  # BDS
# import datetime
import math
import os
# 文件格式设置
pd.set_option('display.width', 6666)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大列，None为显示所有列

# 参数设置
save_year = 2012
date_start = int(str(save_year)+"000")

if save_year % 4 == 0:
    year_days = 366  # 365为年度; 139适用于"5.19"; 334+31适用于13年
else:
    year_days = 365

start_count = -1  # 刘家园超出次数，没完成

API_KEY_LIST = ["APIKEY1", "APIKEY2"]

coordinate_file_path = "D:\\毕业论文程序\\MODIS\\坐标\\"
output_file_path = "D:\\毕业论文程序\\气象数据\\数据\\逐时\\%s\\" % save_year  # 气象数据存储路径
error_information_path = "D:\\毕业论文程序\\气象数据\\报错\\"  # 报错信息输出路径
time_out = 30  # 超时设置,10秒太短

# 批量导入监测站坐标
# JCZ_file = pd.read_excel("监测站坐标toDarkSkyAPI.xlsx")
JCZ_file = pd.read_excel(coordinate_file_path+"监测站坐标toDarkSkyAPI.xlsx")  # 监测站坐标toDarkSkyAPI
JCZ = []
for i in range(len(JCZ_file)):
    exec('JCZ%s = [JCZ_file["经度"][i],JCZ_file["纬度"][i],JCZ_file["城市"][i]+"-"+JCZ_file["监测点名称"][i]]' % i)
    exec("JCZ.append(JCZ%s)" % i)  # exec可以执行字符串指令

# 一年日期
time_list = []
date_int = []
for j in range(year_days):
    date_start += 1
    date = str(date_start)  # 如2018123
    date = time.strptime(date, '%Y%j')
    date = date[0], date[1], date[2]
    time_list.append(date)

# 基本信息
print("监测站个数:", len(JCZ_file), "天数:", len(time_list),
      "即" + str(time_list[0]) + "至" + str(time_list[-1]))

# 主程序
global t


def get_outcome(date_time):
    # 定义气象数据获取函数. 可选项:中文语言lang=["zh"]
    monitoring_station = forecast(*MonitoringStation, time=date_time, timeout=time_out)  # 超时报错设置
    darksky_outcome = monitoring_station['hourly']["data"]  # 输出一天24小时的数据,调用一次API
    # 第一天0时至23时
    # print(coordinate[3], monitoring_station['hourly']["data"]) 数据内容
    # 输出到文件
    outcome.append(darksky_outcome)
    return outcome


# 设置计数
i = start_count

# 监测站
for jcz in JCZ:
    outcome = []
    error = []
    # 一年循环
    for time in time_list:
        i += 1
        API_KEY = API_KEY_LIST[math.floor(i / 1000)]
        print(i, API_KEY)
        coordinate = API_KEY, jcz[1], jcz[0], jcz[2]  # API_KEY,纬度,经度,监测站,注意格式是先"纬度"后"经度"
        MonitoringStation = coordinate[0:3]  # API_KEY、纬度、经度
        # noinspection PyBroadException
        try:
            t = dt(time[0], time[1], time[2], 00).isoformat()
            get_outcome(t)
            # 进度
            print("完成:%s" % coordinate[3], t)
        except Exception as e:
            print("报错:%s" % coordinate[3], t, "内容为:", e)
            error.append(t)  # 保存报错日期
    # print("old", error)
    # 报错日期循环
    print("接下来执行报错日期数据重新获取")
    count_error = 0
    print("%s 未获取数据的天数:" % coordinate[3], len(error))
    while count_error != 2:  # 多次报错则放弃爬取
    # while len(error) != 0:  # 有报错信息则重新爬去,直到全部爬取
        count_error += 1
        error_update = []
        for error_time in error:
            i += 1
            API_KEY = API_KEY_LIST[math.floor(i / 1000)]
            print(i, API_KEY)
            coordinate = API_KEY, jcz[1], jcz[0], jcz[2]  # API_KEY,纬度,经度,监测站,注意格式是先"纬度"后"经度"
            MonitoringStation = coordinate[0:3]  # API_KEY、纬度、经度
            # print(error_time)
            print("重新获取%s" % coordinate[3], error_time)
            # noinspection PyBroadException
            try:
                get_outcome(error_time)
                print("重新获取成功")
            except Exception as e:
                print("重新获取失败,稍后重新获取,失败原因:", e)
                error_update.append(error_time)
        error = error_update
    df = []
    for item in outcome:
        item = eval(str(item))
        item = pd.DataFrame(item)
        df.append(item)
    if len(df) != 0:
        df_output = pd.concat(df, sort=True)
        df_output['time'] = df_output['time'].map(lambda x: dt.fromtimestamp(x))  # datetime.datetime
        df_output = df_output.sort_values("time", ascending=True)
        df_output = df_output.set_index('time')
        df_output.to_excel(output_file_path+"%s.xlsx" % coordinate[3])
    if len(error) != 0:  # 空列表不输出,代码经过修改已经没有"error"列表了,以防万一保存了该部分代码
        error = pd.DataFrame(error)
        # error.columns = ["Index", '日期']
        error.to_excel(error_information_path+"%s报错.xlsx" % coordinate[3])

# 自动关机
print("程序已完成," + str(60) + '秒后将会关机')
#os.system('shutdown -s -f -t 60')
