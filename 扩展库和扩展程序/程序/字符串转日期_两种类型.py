# -*- coding: utf-8 -*-
# 时间    : 2019/1/22 17:44
# 作者    : xcl

'''
字符串转日期
'''
# 方法一,字符串类型
import time
q = time.strptime('2018014', '%Y%j')
t = q
t = time.strftime("%Y-%m-%d ", t)
print(t.__class__)

# 方法二,时间类型
import datetime
import time
weekday = time.strptime('2018014', '%Y%j')
weekday = time.strftime("%Y-%m-%d", weekday)
weekday = datetime.datetime.strptime(weekday, '%Y-%m-%d').date()
print(weekday.__class__)




weekday = time.strptime('20180530', '%Y%m%d')
weekday = time.strftime("%Y-%m-%d", weekday)
weekday = datetime.datetime.strptime(weekday, '%Y-%m-%d').date()
print(weekday.__class__, weekday)