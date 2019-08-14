
import pandas as pd
import numpy as np

def main():
    global t
    class test(object):
        def __init__(self):
            pass
    t = test()
    for i in range(1,9):
        setattr(t, "a"+str(i), [])
    #print(t.__dict__)
    #print(t)
    #print(t.a1.__class__)


main()

c= "adsas"

for i in range(1,9):
    exec('t.a%s.append(c)' % i)

for i in range(1,9):
    exec('print(t.a%s)' % i)