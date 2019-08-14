# -*- coding: utf-8 -*-
# 日期: 2019/3/16 23:41
# 作者: xcl
# 工具：PyCharm

import pandas as pd
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from sklearn.model_selection import train_test_split  # 划分
import matplotlib.pyplot as plt

model_file = "F:\\毕业论文程序\\缓存\\1-net.model"
data_file = "F:\\毕业论文程序\\整合数据\\各地区\\日均\\总地区.xlsx"
data = pd.read_excel(data_file)

# 自变量列
independent = ["AOD值", 'cloudCover', 'dewPoint', 'humidity', 'precipAccumulation', 'precipIntensity', 'pressure',
               'temperature', 'uvIndex', 'visibility', 'windSpeed']

# 因变量
dependent = ["日均PM2.5"]

x_train, x_test, y_train, y_test = train_test_split(data[independent], data[dependent], train_size=0.7, test_size=0.3,
                                                    random_state=0)

x_test = x_test.values
x_train = x_train.values
y_test = y_test.values
y_train = y_train.values


# 隐藏层
model = Sequential()
model.add(Dense(input_dim=11, units=22))
model.add(Activation("relu"))
model.add(Dense(input_dim=22, units=1))

model.compile(loss="mean_squared_error", optimizer="adam")  # 编译模型
model.fit(x_train, y_train, epochs=10000, batch_size=100)  # 训练
model.save_weights(model_file)

# 预测
data_pre = abs(model.predict(x_test) - y_test)
print(data_pre.mean())

