# MODIS04_3K_PM25
  Environmental Science: Predicting PM with MODIS data(AOD)  
  使用NASA MODIS Aqua/Terra 卫星的气溶胶L2级别数据, 即MOD04_3K, 来预测日均PM.

## 数据来源 DATA
  气溶胶: https://ladsweb.modaps.eosdis.nasa.gov/search/  
  污染物/空气质量: http://beijingair.sinaapp.com/  
  气象数据: https://darksky.net/dev  
  程序包: https://www.lfd.uci.edu/~gohlke/pythonlibs/  
  特别感谢数据提供者!
## 气溶胶文件夹 Aerosol
#### 空间转换模块.py：
  批量读取.hdf文件,针对各个监测站经纬度获取三个不同长度半径的同心圆,再按照角度划分为不同区域.
#### 四种插值方法和结果.py：
  批量;在时间上使用KNN和ewm方法进行插值; 空间上使用IDW和Iterative方法进行插值.
  
## 污染物文件夹 Pollution
#### 日均污染物数据整理.py：
  批量读取城市/站点空气质量数据; 可按监测站输出空气质量时间序列数据.
#### 四种插值方法和结果.py：
  批量;在时间上使用KNN和ewm方法进行插值; 空间上使用IDW和Iterative方法进行插值.
#### 权重融合_熵权法.py:
  批量,按照熵权法对四种插值方法进行融合.
  
## 气象数据文件夹 DarkSky API
#### DarkSkyAPI日均/逐时.py：
  批量爬取对应经纬度的天气历史数据和天气预报数据.
#### 日均/逐时气象数据处理.py, 逐时气象数据均值处理.py:
  批量处理气象数据格式, 如时间范围删选, 时间格式调整, 逐时均值.

## 建模文件夹 Model
  初步建立: 单输入,多输入模型; 线性回归; MPL神经网络; Boosting&Bagging; KFold交叉验证.
  
## 坐标文件夹 Longitude&Latitude
  全国监测站名称, 所属城市, 编码, 经纬度.

## 扩展库和扩展程序
#### 库
  气象数据:DarkSkyAPI, 数据调用依赖库[darkskylib-master ], 详细内容请参考https://github.com/lukaskubis/darkskylib
  气溶胶数据: HDF文件, 读取依赖库[python_hdf]
  插值: 插值库fancyimpute安装遭遇失败时, 如'failed build', 'get microsoft build tools from..', 可以先安装[scs][ecos]
#### 程序
  学习过程中遇到的问题, 对应的整理出了解决方法..
  
# 感谢
  非环境科学领域专业学生, 对该内容感到兴趣便着手进行了.
  代码上存在运算效率不够高, 繁琐的问题也欢迎大家给我提建议, 十分感谢.
  加油, (ง •_•)ง~
  
  
  
 #### 邮箱 xunchanglu@vip.163.com
