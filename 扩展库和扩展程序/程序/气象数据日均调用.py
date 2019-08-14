# -*- coding: utf-8 -*-
# 日期: 2019/3/11 10:37
# 作者: xcl
# 工具：PyCharm

from darksky import forecast
from datetime import date, timedelta

BOSTON = 42.3601, 71.0589

weekday = date.today()
with forecast('a5fc93a6781f6d55e7899ae443acd876', *BOSTON) as boston:
    # print(boston.daily.data, end='\n---\n')
    print(boston["daily"]["data"])