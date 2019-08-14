# -*- coding: utf-8 -*-
# 日期: 2019/3/24 23:17
# 作者: xcl
# 工具：PyCharm

import pandas as pd
from scipy.stats import pearsonr
import numpy as np

data = "C:\\Users\\Administrator.SC-201902221855\\Desktop\\电影指标处理.xlsx"

data = pd.read_excel(data)

# data["豆瓣网评分"] = data["豆瓣网评分"].map(lambda x: float(x))

# 删除评分为“无”
indexs = data[data["豆瓣网评分"] == "无"].index
data = data.drop(index=indexs)
# 删除空列
data = data[data["豆瓣网评分"] >= 0]

# 更换单位


def replace_df(x):
    x = str(x)
    if "亿" in x:
        x = x.replace("亿", "")
        x = float(x)
        x = x*10000
    x = str(x)
    if "万" in x:
        x = x.replace("万", "")
        x = float(x)
    return x


data["总票房"] = data["总票房"].map(lambda x: replace_df(x))
data["首映日票房（万）"] = data["首映日票房（万）"].map(lambda x: replace_df(x))
# 手动删除了一些迷之空行
# print(data.isnull().sum())

# 计算 皮尔森相关性
x_list = ['年度排名', '历史排名',  '首映日票房（万）', '上映时间.1', '上映两周前影片360指数', '上映当天影片360指数', '上映两周后影片360指数', '指数均值',
          '豆瓣网评分', '豆瓣评影人数']

# Index(['年度排名', '历史排名', '电影名称', '总票房', '总票房（元）', '首映日票房（万）', '上映时间', '放映截止',
#        '上映时间.1', '上映两周前影片360指数', '上映当天影片360指数', '上映两周后影片360指数', '指数均值',
#        '豆瓣网评分', '豆瓣评影人数', '豆瓣定义影片类型', '导演', '第一主演', '第二主演', '影片类型', '放映总天数',
#        '百度搜索指数', '制作公司', '总人次', '总场次', '上映年份'],
#       dtype='object')

y = list(data['总票房'])
y = np.array(y, dtype='float_')
for xx in x_list:
    data_xx = data[xx].map(lambda x: float(x))
    data_xx = np.array(data_xx, dtype='float_')
    # print(data_xx)
    # print(xx, pearsonr(data_xx, y))  # 输出(r,p)
    print(pearsonr(data_xx, y)[0])
