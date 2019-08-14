# -*- coding: utf-8 -*-
# 日期: 2019/3/18 10:43
# 作者: xcl
# 工具：PyCharm


import datetime
def get_day(date, step=0):
    """获取指定日期date(形如"xxxx-xx-xx")之前或之后的多少天的日期, 返回值为字符串格式的日期"""
    l = date.split("-")
    y = int(l[0])
    m = int(l[1])
    d = int(l[2])
    old_date = datetime.datetime(y, m, d)
    new_date = (old_date + datetime.timedelta(days=step)).strftime('%Y-%m-%d')
    print(new_date)
    return new_date
get_day('2019-3-1', -1)  # 往前一天 2019-01-30
get_day('2019-01-31', 1)  # 往后一天 2019-02-01

