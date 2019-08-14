# -*- coding: utf-8 -*-
# 日期: 2019/3/20 14:40
# 作者: xcl
# 工具：PyCharm


from darksky import forecast  # DarkSkyAPI

key = "****"

location = key, 38.9194, 117.157
from datetime import datetime as dt
t = dt(2018, 2, 12, 12).isoformat()
location = forecast(*location, time=t)
print(location.time)
print(location["daily"])
