# -*- coding:utf-8 -*- 
# 日期：2019/2/8 16:12
# 作者：xcl
# 工具：PyCharm
# 修改了原获取气象数据的DarkSkyAPI的代码,因此此代码弃用
# 此代码尚未完成,请不要使用

from darksky import forecast
import pandas as pd
import numpy as np
import os
import datetime

# 参数设置
input_file_path = 'C:\\Users\\寻常鹿\Desktop\\气象数据\\报错test\\'
output_file_path = 'C:\\Users\\寻常鹿\Desktop\\气象数据\\补充\\'
year_days = 365
date_start = 2018000
API_KEY = "740c4d0fbd102f83a7753032c769b2b5"

# 批量读取文件
file_name = os.listdir(input_file_path)  # 文件名

coordinate_JCZ = pd.read_excel("监测站坐标to气象.xlsx", sheet_name="汇总", )
coordinate_JCZ = np.array(coordinate_JCZ)

data = pd.read_excel(input_file_path+file_name[0])

schedule_whole = 0
global t
for name in file_name:
    data = pd.read_excel(input_file_path+name)
    schedule_current = 0
    outcome = []
    error = []
    print(name)
    for item in coordinate_JCZ:
        # print(item)
        dizhi = item[2]+"-"+item[1]  # 如 北京-东四
        schedule_whole += 1
        schedule_current += 1
        if dizhi == name.replace("报错.xlsx", ""):
            MonitoringStation = API_KEY, item[4], item[3]  # API_KEY,纬度,经度,监测站,注意格式是先"纬度"后"经度"
            print(dizhi, ":", MonitoringStation)
            for date in data["日期"]:
                try:
                    # t = dt(time[0], time[1], time[2], 00).isoformat()
                    t = date
                    monitoring_station = forecast(*MonitoringStation, time=t, timeout=30)  # 超时报错设置
                    DarkSky_outcome = monitoring_station['hourly']["data"]  # 输出一天24小时的数据,调用一次API
                    # print(coordinate[3], monitoring_station['hourly']["data"]) 数据内容
                    # 输出到文件
                    outcome.append(DarkSky_outcome)
                    # 进度
                    print("完成:%s" % dizhi, "时间:%s" % date)
                except Exception as e:
                    print(t, "报错")
                    error.append(t)
    df = []
    for element in outcome:
        element = eval(str(element))
        element = pd.DataFrame(element)
        df.append(element)
    if len(df) != 0:
        df_output = pd.concat(df, sort=True)
        df_output['time'] = df_output['time'].map(lambda x: datetime.datetime.fromtimestamp(x))
        df_output = df_output.set_index('time')
        df_output.to_excel(output_file_path+"%s.xlsx" % name.replace("报错.xlsx", ""))
    if len(error) != 0:  # 空列表不输出
        error = pd.DataFrame(error)
        error.to_excel(output_file_path+"%s报错.xlsx" % name.replace("报错.xlsx", ""))
