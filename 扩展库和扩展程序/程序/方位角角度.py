# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/7/15 13:02


import math
import pandas as pd
import numpy as np
from math import radians, sin, cos, degrees, atan2


def getDegree(latA, lonA, latB, lonB):
    """
    Args:
        point p1(latA, lonA)
        point p2(latB, lonB)
    Returns:
        bearing between the two GPS points,
        default: the basis of heading direction is north
    """
    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)
    dLon = radLonB - radLonA
    y = sin(dLon) * cos(radLatB)
    x = cos(radLatA) * sin(radLatB) - sin(radLatA) * cos(radLatB) * cos(dLon)
    brng = degrees(atan2(y, x))
    brng = (brng + 360) % 360
    return brng


c = getDegree(0, 0, -4,-4)

print(c)

# 网上相关代码'def azimuthAngle( x1,  y1,  x2,  y2)' 是错误的, 不要使用.