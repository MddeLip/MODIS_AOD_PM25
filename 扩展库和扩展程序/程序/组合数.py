# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/7/5 13:21
import numpy as np

from scipy.special import comb, perm
import numpy as np
c = np.random.randint(1,1000,size=10)

X = c
X = [45787,64579,72688,84824,93538,91378,103743,]

rd = [3.7938589742072177 ,1.4666045920105375 ,1.294721579999216, 1.1120484810346465 ,1.029515462139862, 1.0725683868279428 ,1.0]




outcome = []
'''########test1!
for r in [1,1.5,2,2.5,3,3.5,4,4.5,5]:
    listr = []
    print("r=", r)
    for k in range(1, len(X)+1):
        x0 = 0
        fenmu1 = 0
        for i in range(k, len(X)+1):
            CCC = comb(i-k+r-1, i-k)
            fenmu1 = fenmu1 + CCC
            x0 = x0 + comb(i-k+r-1, i-k)*X[i-1]
        res=x0/fenmu1
        listr.append(res)
    outcome.append(listr)

import pandas as pd
outcome = pd.DataFrame(outcome)
outcome.to_excel("out.xlsx")
'''



r = rd[7]
listr = []
#print("r=", r)
for k in range(1, len(X)+1):
    x0 = 0
    fenmu1 = 0
    for i in range(k, len(X)+1):
        CCC = comb(i-k+r-1, i-k)
        fenmu1 = fenmu1 + CCC
        x0 = x0 + comb(i-k+r-1, i-k)*X[i-1]
    res=x0/fenmu1
    print(res)
    #listr.append(res)
#outcome.append(listr)
