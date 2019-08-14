# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/7/18 11:12


from scipy import stats
import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt



save_year = 2016

date_start = 2013000

tiaojian = save_year % 4
print(tiaojian)

#####################################
if tiaojian == 0:
    days=365
else:
    days=10


print(days)


######################################

save_year = 2013

dat = str(save_year)+"000"

print(int(dat))
