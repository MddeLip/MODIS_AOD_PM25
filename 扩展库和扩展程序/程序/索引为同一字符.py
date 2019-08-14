# -*- coding:utf-8 -*- 
# 日期：2019/2/15 15:29
# 作者：xcl
# 工具：PyCharm


import pandas as pd
import numpy as np


df = pd.DataFrame(np.random.randn(8,5))
df["ddd"] = 123

print(df)



