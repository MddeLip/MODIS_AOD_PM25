# -*- coding: utf-8 -*-
# 日期: 2019/3/7 9:14
# 作者: xcl
# 工具：PyCharm
import pandas as pd
import numpy as np


df1=pd.DataFrame({'key':['a','b','c'],'data1':[1,2,3],'data2':[4,5,6]})
df1 = df1.set_index('key')

df2=pd.DataFrame({'key':['b','c','d'],'data1':[1,2,3],'data2':[4,5,6]})
df2 = df2.set_index('key')
c = pd.concat([df1,df2], axis=1)

print(c)