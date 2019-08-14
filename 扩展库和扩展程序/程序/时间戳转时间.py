# -*- coding: utf-8 -*-
# 时间    : 2019/1/25 21:54
# 作者    : xcl

import datetime

#1365300000
#1365303600


unix_ts = 1514736000
times = datetime.datetime.fromtimestamp(unix_ts)
print(times)
