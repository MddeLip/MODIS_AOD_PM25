# -*- coding: utf-8 -*-
# 日期: 2019/3/6 21:23
# 作者: xcl
# 工具：PyCharm

import pandas as pd
import os
# 参数设置
location = "北京"
input_file_path = "F:\\毕业论文程序\\整合数据\\各监测站\\combine\\"  # HDF文件位置 TTT
output_file_path = "F:\\毕业论文程序\\整合数据\\各地区\\combine\\"  # 结果的输出位置

# 批量读取
file_name = os.listdir(input_file_path)  # 文件名
for name in file_name:
    if location in name:
        print(name)
