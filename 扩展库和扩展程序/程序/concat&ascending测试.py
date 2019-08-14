# -*- coding:utf-8 -*- 
# 日期：2019/2/9 20:51
# 作者：xcl
# 工具：PyCharm

import pandas as pd

a = [[1, 3, 3], [4, 1, 6], [7, 8, 9]]
a = pd.DataFrame(a)
a.columns = ["A", "B", "C"]

b = [[3, 5, 8], [2, 7 , 3], [6, 1, 5]]
b = pd.DataFrame(b)
b.columns = ["A", "B", "C"]

c = pd.concat([a, b], sort=True, ignore_index=True)

c = c.sort_values("B", ascending=True)
print(c)
