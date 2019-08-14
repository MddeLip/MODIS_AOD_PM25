# -*- coding: utf-8 -*-
# 日期: 2019/3/17 22:18
# 作者: xcl
# 工具：PyCharm

import pandas as pd
import time
input = "F:\\毕业论文程序\\整合数据\\各地区\\日均\\总地区toR.xlsx"

data = pd.read_excel(input)


# 字符类型的时间
def get_sjc(x):
    x = str(x)
    timeArray = time.strptime(x, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp  # 1381419600


data["日期"] = data["日期"].map(lambda x: get_sjc(x))

data.set_index("日期")
data.to_excel(input)
