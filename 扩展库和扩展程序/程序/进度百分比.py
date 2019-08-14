# -*- coding: utf-8 -*-
# 时间    : 2019/1/24 8:52
# 作者    : xcl


file_name = ["mike", 'mail', 'neal', 'nick', 'trump', 'matte', 'lucky', "brother", "sister", "school"]
file_size = ["A15", 'A99', 'A6', 'A23', 'A44', 'A76', 'A419', "A69", "A779", "A54"]


k = 0
for item in file_name:
    j = 0
    for element in file_size:
        j = j + 1
        k = k + 1
        #print("j", j)
        print("当前进度", (j/len(file_size)), "总进度", k/(len(file_size)*len(file_name)))
