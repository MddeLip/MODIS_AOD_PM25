# -*- coding: utf-8 -*-
# 时间    : 2019/1/16 23:51
# 作者    : xcl

import sys
import os
import time


# shutdown computer after time_diff seconds
def main(seconds):
    print(str(seconds) + u' 秒后将会关机...')
    time.sleep(seconds)
    print('关机啦。。。')
    os.system('shutdown -s -f -t 1')

# -*- coding: utf-8 -*-
# 时间    : 2019/1/16 11:03
# 作者    : xcl


'''
                            增加经纬度计算距离
                            忽略空列表计算均值而产生的warnings
'''

#因为采集AOD时会出现缺失值，因此计算范围内均值时会出现warnings
#导入以下库来忽略该warnings
import warnings
warnings.filterwarnings('ignore')
#相关库
from math import radians, cos, sin, asin, sqrt
#import xlwt
import pandas as pd
import numpy as np
from pyhdf.SD import SD, SDC
# #import pprint
import datetime

#计算耗时
starttime = datetime.datetime.now()
#定义经纬度距离公式
def geodistance(lng1,lat1,lng2,lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlon=lng2-lng1
    dlat=lat2-lat1
    a=sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    dis=2*asin(sqrt(a))*6371*1000
    return(dis)

import os
dir_str = r"C:\\Users\\Administrator\\Desktop\\MODIS\\HDF"
file_name = os.listdir(dir_str)
file_dir = [os.path.join(dir_str, x) for x in file_name]
#print(file_dir)#,file_name)

outcome = "C:\\Users\\Administrator\\Desktop\\MODIS\\outcome.xlsx"
file_handle=open('1.txt',mode='a+')

#参数设置
#经纬度转换为的距离范围，监测站3KM半径范围内为观测区域
r = 3000
#监测站
### 北京市
JCZ1 = [116.366,39.8673,"北京-万寿西宫"]
JCZ2 = [116.170,40.2865,"北京-定陵"]
JCZ3 = [116.434,39.9522,"北京-东四"]
JCZ4 = [116.434,39.8745,"北京-天坛"]
JCZ5 = [116.473,39.9716,"北京-农展馆"]
JCZ6 = [116.361,39.9425,"北京-官园"]
JCZ7 = [116.315,39.9934,"北京-海淀区万柳"]
JCZ8 = [116.720,40.1438,"北京-顺义新城"]
JCZ9 = [116.644,40.3937,"北京-怀柔区"]
JCZ10= [116.230,40.1952,"北京-昌平区"]
JCZ11= [116.407,40.0031,"北京-奥体中心"]
JCZ12= [116.225,39.9279,"北京-古城"]
### 天津市
JCZ13= [117.151,39.0970,"天津-市监测中心"]
JCZ14= [117.193,39.1730,"天津-南口路"]
JCZ15= [117.145,39.1654,"天津-勤俭路"]
JCZ16= [117.184,39.1205,"天津-南京路"]
JCZ17= [117.237,39.1082,"天津-大直沽八号路"]
JCZ18= [117.202,39.0927,"天津-前进路"]
JCZ19= [117.1837,39.2133,"天津-北辰科技园区"]
JCZ20= [117.269,39.1337,"天津-天山路"]
JCZ21= [117.307,39.0877,"天津-跃进路"]
JCZ22= [117.707,39.0343,"天津-第四大街"]
JCZ23= [117.457,39.8394,"天津-永明路"]
JCZ24= [117.401,39.1240,"天津-航天路"]
JCZ25= [117.764,39.1587,"天津-汉北路"]
JCZ26= [117.157,38.9194,"天津-团泊洼"]
###河北省
JCZ27= [114.4548,38.0513,"河北石家庄-职工医院"]
JCZ28= [114.6046,38.0398,"河北石家庄-高新区"]
JCZ29= [114.5019,38,1398,"河北石家庄-西北水源"]
JCZ30= [114.4586,38.00583,"河北石家庄-西南高教"]
JCZ31= [114.5331,38.01778,"河北石家庄-世纪公园"]
JCZ32= [114.5214,38.0524,"河北石家庄-人民会堂"]
JCZ33= [114.3541,37.9097,"河北石家庄-封龙山"]
JCZ34= [118.1662,39.6308,"河北唐山-供销站"]
JCZ35= [118.144,39.643,"河北唐山-雷达站"]
JCZ36= [118.1853,39.6407,"河北唐山-物资局"]
JCZ37= [118.2185,39.6679,"河北唐山-陶瓷公司"]
JCZ38= [118.1838,39.65782,"河北唐山-十二中"]
JCZ39= [118.1997,39.6295,"河北唐山-小山"]
JCZ40= [119.5259,39.8283,"河北秦皇岛-北戴河环保局"]
JCZ41= [119.7624,40.0181,"河北秦皇岛-第一关"]
JCZ42= [119.6023,39.9567,"河北秦皇岛-监测站"]
JCZ43= [119.607,39.9358,"河北秦皇岛-市政府"]
JCZ44= [119.5369,39.9419,"河北秦皇岛-建设大厦"]
JCZ45= [114.5129,36.61763,"河北邯郸-环保局"]
JCZ46= [114.5426,36.6164,"河北邯郸-东污水处理厂"]
JCZ47= [114.5035,36.5776,"河北邯郸-矿院"]
JCZ48= [114.4965,36.61981,"河北邯郸-丛台公园"]
JCZ49= [115.493,38.8632,"河北保定-游泳馆"]
JCZ50= [115.5223,38.8957,"河北保定-华电二区"]
JCZ51= [115.4713,38.9108,"河北保定-接待中心"]
JCZ52= [115.4612,38.8416,"河北保定-地表水厂"]
JCZ53= [115.442,38.8756,"河北保定-胶片厂"]
JCZ54= [115.5214,38.8707,"河北保定-监测站"]
JCZ55= [114.8985,40.8367,"河北张家口-人民公园"]
JCZ56= [114.892,40.79481,"河北张家口-探机厂"]
JCZ57= [114.8814,408115,"河北张家口-五金库"]
JCZ58= [114.9032,40.7688,"河北张家口-世纪豪园"]
JCZ59= [114.904,40.8725,"河北张家口-北泵房"]
JCZ60= [117.9664,409161,"河北承德-铁路"]
JCZ61= [117.9525,40.9843,"河北承德-中国银行"]
JCZ62= [117.963,40.9359,"河北承德-开发区"]
JCZ63= [117.8184,40.9733,"河北承德-文化中心"]
JCZ64= [117.9384,41.0112,"河北承德-离宫"]
JCZ65= [116.6838,39.5178,"河北廊坊-药材公司"]
JCZ66= [116.7729,39.5747,"河北廊坊-开发区"]
JCZ67= [116.715,39.5571,"河北廊坊-环境监测监理中心"]
JCZ68= [116.7464,39.5343,"河北廊坊-北华航天学院"]
JCZ69= [116.8854,38.2991,"河北沧州-沧县城建局"]
JCZ70= [116.8584,38.3254,"河北沧州-电视转播站"]
JCZ71= [116.8709,38.3228,"河北沧州-市环保局"]
JCZ72= [115.6951,37.7575,"河北衡水-电机北厂"]
JCZ73= [115.6426,37.7379,"河北衡水-市监测站"]
JCZ74= [115.6906,37.739,"河北衡水-市环保局"]
JCZ75= [114.4821,37.0967,"河北邢台-达活泉"]
JCZ76= [114.5261,37.0533,"河北邢台-邢师高专"]
JCZ77= [114.5331,37.0964,"河北邢台-路桥公司"]
JCZ78= [114.4854,37.062,"河北邢台-市环保局"]
###山东省









































JCZ = [JCZ1,JCZ2,JCZ3,JCZ4,JCZ5,JCZ6,JCZ7,JCZ8,JCZ9,JCZ10,JCZ11,JCZ12,JCZ13,JCZ14,JCZ15,JCZ16,JCZ17,JCZ18,JCZ19,JCZ20
    , JCZ21,JCZ22,JCZ23,JCZ24,JCZ25,JCZ26,JCZ27,JCZ28,JCZ29,JCZ30,JCZ31,JCZ32,JCZ33,JCZ34,JCZ35,JCZ36,JCZ37,JCZ38,JCZ39
    ,JCZ40,JCZ41,JCZ42,JCZ43,JCZ44,JCZ45,JCZ46,JCZ47,JCZ48,JCZ49,JCZ50,JCZ51,JCZ52,JCZ53,JCZ54,JCZ55,JCZ56,JCZ57,JCZ58
    ,JCZ59,JCZ60,JCZ61,JCZ62,JCZ63,JCZ64,JCZ65,JCZ66,JCZ67,JCZ68,JCZ69,JCZ70,JCZ71,JCZ72,JCZ73,JCZ74,JCZ75,JCZ76,JCZ77
    ,JCZ78,JCZ78]
#print("监测站总数:",len(JCZ),"个")
JCZ = np.unique(JCZ)#去重
print("监测站总数:",len(JCZ),"个")

# 文件读取
aod_outcome_list = []
for hdf in file_dir:
    HDF_FILR_URL = hdf
    file = SD(HDF_FILR_URL)
    # print(file.info())
    datasets_dic = file.datasets()
    '''
    for idx, sds in enumerate(datasets_dic.keys()):
        print(idx, sds)
    '''
    sds_obj1 = file.select('Longitude')  # select sds
    sds_obj2 = file.select('Latitude')  # select sds
    sds_obj3 = file.select('Optical_Depth_Land_And_Ocean')  # select sds
    longitude = sds_obj1.get()  # get sds data
    latitude = sds_obj2.get()  # get sds data
    aod = sds_obj3.get()  # get sds data
    longitude = pd.DataFrame(longitude)
    latitude = pd.DataFrame(latitude)
    aod = pd.DataFrame(aod)
    for item in JCZ:
        aodlist = []
        for i in range(longitude.shape[1]):  # 列
            for j in range(longitude.shape[0]):  # 行
                d = geodistance(longitude[i][j],latitude[i][j],item[0],item[1])
                '''
                #方法二，弃用
                vec1 = np.array([longitude[i][j], latitude[i][j]])
                vec2 = np.array([item[0], item[1]])
                d = np.linalg.norm(vec1 - vec2)# 欧式距离
                #d = ((longitude[i][j]) - item[0])** 2 + ((latitude[i][j]) - item[1]) ** 2 # 欧式距离
                '''
                if d > 0 and d < r and aod[i][j] > 0:
                    aodlist.append(aod[i][j])
        #print("%s文件的%s监测站AOD值:" % (hdf,item[2]), np.average(aodlist))  # 批量改名，一次输出
        aod_outcome = "%s文件" % hdf,"%s" % item[2], np.average(aodlist)
        print("完成 %s文件" % hdf,"%s" % item[2])
        aod_outcome_list.append(aod_outcome)
#print(aod_outcome_list)#结果查看
aod_outcome_list_v2 = []
for item in aod_outcome_list:
    item = pd.Series(item)
    #替换掉冗余字符
    item[0] = item[0].replace("C:\\\\Users\\\\Administrator\\\\Desktop\\\\MODIS\\\\HDF", "")
    item[0] = item[0].replace("\\", "")
    item[0] = item[0].replace(".hdf文件", "")
    item = np.array(item)
    aod_outcome_list_v2.append(item)
#避免字符串省略，四行设置都需要
pd.set_option('display.max_rows',None)#行
pd.set_option('display.max_columns',1000)#列
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)

#写入TXT
aod_outcome_list_v2 = pd.DataFrame(aod_outcome_list_v2)
aod_outcome_list_v2.columns = ['日期', '监测站', 'AOD值']
file=open('data.txt','w')
file.write(str(aod_outcome_list_v2));
file.close()
# 计算所用时间
endtime = datetime.datetime.now()
print(endtime - starttime)

file=open('TIME.txt','w')
file.write(str(endtime - starttime));
file.close()





#运行完关机

import os
import time


def shutdown_computer(seconds):
    print(str(seconds) + u' 秒后将会关机...')
    time.sleep(seconds)
    print('关机啦。。。')
    os.system('shutdown -s -f -t 1')

shutdown_computer(60)
if __name__ == '__main__':
    main(6000)
