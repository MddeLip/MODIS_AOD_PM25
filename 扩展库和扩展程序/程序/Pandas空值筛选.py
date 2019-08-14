# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 11:10


# 库
from multiprocessing import Process  # 多线程,提高CPU利用率
import copy
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np
import os

a = [[np.nan, 2, np.nan], [np.nan, 5, 6], [7, 8, 9]]

a = pd.DataFrame(a)

a.columns = ["A", "B", "C"]

d = a[(a["A"] == np.nan) & (a["B"] == np.nan) & (a["C"] == np.nan)]

d2 = a[pd.isnull(a["A"]) & pd.isnull(a["C"])]

print(a, d2, sep="\n")
