# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 11:10


# 库
from multiprocessing import Process  # 多线程,提高CPU利用率
import copy
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np
from fancyimpute import KNN, IterativeImputer  # 方法创建新的数据框,不覆盖原始数据
import os

# 路径
input_file_path_pollution = "D:\\毕业论文程序\\污染物浓度\\整理\\全部污染物\\多年合一\\"
merge_output_file_path = "D:\\毕业论文程序\\污染物浓度\\插值模块\\Merge\\多年合一\\"
JCZ_info = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx", sheet_name="汇总")  # 152个
JCZ_info["监测站"] = JCZ_info["城市"] + "-" + JCZ_info["监测点名称"]


def get4method(xx152):
    # 地理距离
    def geo_distance(lng1_df, lat1_df, lng2_df, lat2_df):
        lng1_df, lat1_df, lng2_df, lat2_df = map(radians, [lng1_df, lat1_df, lng2_df, lat2_df])
        d_lon = lng2_df - lng1_df
        d_lat = lat2_df - lat1_df
        a = sin(d_lat / 2) ** 2 + cos(lat1_df) * cos(lat2_df) * sin(d_lon / 2) ** 2
        dis = 2 * asin(sqrt(a)) * 6371.393 * 1000  # 地球半径
        return dis  # 输出结果的单位为“米”

    # 空间局部: 难以插值是因为大部分地区及其临近地区同一污染物值可能会一同缺失.
    def get_IDW(input_data):
        for pollution in ["PM25", "PM10", "SO2", "NO2", "O3", "CO"]:  # 确定污染物列
            for indx in input_data.index:  # 获取索引
                res_list = []
                weight_list = []
                if pd.isnull(input_data[pollution][indx]):  # 开始循环
                    for item_idw in JCZ_info["监测站"]:  # 获取距离,定义权重
                        if item_idw != name:
                            lng2 = JCZ_info[JCZ_info["监测站"] == item_idw]["经度"]
                            lat2 = JCZ_info[JCZ_info["监测站"] == item_idw]["纬度"]
                            dis_1 = geo_distance(lng1, lat1, lng2, lat2)  # 两站地理距离
                            if dis_1 <= 50000:
                                data_to_add_in_1 = pd.read_excel(input_file_path_pollution + item_idw + ".xlsx")
                                data_to_add_in_1 = data_to_add_in_1.set_index("日期")  # 需要日期为索引,方便下面添加
                                if indx in data_to_add_in_1.index and pd.notnull(data_to_add_in_1[pollution][indx]):
                                    weight_list.append(dis_1)
                    weight_sum = np.sum(np.array(weight_list))  # 总距离,权重分母
                    for item_idw_2 in JCZ_info["监测站"]:  # 分配权重
                        if item_idw_2 != name:
                            lng2 = JCZ_info[JCZ_info["监测站"] == item_idw_2]["经度"]
                            lat2 = JCZ_info[JCZ_info["监测站"] == item_idw_2]["纬度"]
                            dis_1 = geo_distance(lng1, lat1, lng2, lat2)  # 两站地理距离
                            if dis_1 <= 50000:
                                data_to_add_in = pd.read_excel(input_file_path_pollution + item_idw_2 + ".xlsx")
                                data_to_add_in = data_to_add_in.set_index("日期")  # 需要日期为索引,方便下面添加
                                if indx in data_to_add_in.index and pd.notnull(data_to_add_in[pollution][indx]):
                                    res = (dis_1 / weight_sum) * data_to_add_in[pollution][indx]
                                    res_list.append(res)
                                    # print("已添加单元格插值:", res)
                    res_output = np.sum(np.array(res_list))  # 上下公式结果若为nan,并不会报错.会让最后的插值为nan.
                    try:
                        input_data[pollution][indx] = res_output
                    except Exception as e:
                        print("缺失严重, 插值未定义:", e)
        print("[IDW]Finished.")
        return input_data

    # 监测站
    jcz_152 = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\站点列表-2018.11.08起_152.xlsx", sheet_name=xx152)
    jcz_152["监测站名称_152"] = jcz_152["城市"] + "-" + jcz_152["监测点名称"]
    for input_file_name in jcz_152["监测站名称_152"]:
        input_file_name = input_file_name + ".xlsx"
        print("========正在计算%s========" % input_file_name)
        # 读取数据源
        data_pollution = pd.read_excel(input_file_path_pollution + input_file_name)
        data_pollution = data_pollution.set_index('日期')
        # 时间局部：最近邻KNN,是使用K行都具有全部特征的样本,使用其他特征的均方差进行加权,判断最接近的时间点.
        data_pollution_KNN = KNN(k=7).fit_transform(data_pollution)
        data_pollution_KNN = pd.DataFrame(data_pollution_KNN)
        # 时间全局: 平滑,常用于股市;创建新的数据框,不会覆盖原始数据
        data_pollution_ewm_mid = pd.DataFrame.ewm(
            self=data_pollution,
            com=0.5,
            ignore_na=True,
            adjust=True).mean()
        data_pollution_ewm = copy.deepcopy(data_pollution)  # 避免覆盖原始数据
        for columname in data_pollution_ewm.columns:
            if data_pollution[columname].count() != len(data_pollution):
                loc = data_pollution[columname][data_pollution[columname].isnull().values == True].index.tolist()
                for nub in loc:
                    data_pollution_ewm[columname][nub] = data_pollution_ewm_mid[columname][nub]

        # 空间
        data_pollution_to_IDW = copy.deepcopy(data_pollution)
        name = str(input_file_name).replace(".xlsx", "")  # 定义相关变量
        lng1 = JCZ_info[JCZ_info["监测站"] == name]["经度"]
        lat1 = JCZ_info[JCZ_info["监测站"] == name]["纬度"]
        # 空间局部: IDW,反距离插值
        data_pollution_IDW = get_IDW(data_pollution_to_IDW)
        # 空间全局: 迭代回归,缺失特征作为y,其他特征作为x
        merge_list = []  # 同一监测站,不同污染物
        for pollution_Iterative in ["PM25", "PM10", "SO2", "NO2", "O3", "CO"]:
            concat_list = []  # 用于添加同污染物,不同监测站的数值
            numb = 0
            for item in JCZ_info["监测站"]:  # 不同于气溶胶插值方法
                if item != name:
                    lng_2 = JCZ_info[JCZ_info["监测站"] == item]["经度"]
                    lat_2 = JCZ_info[JCZ_info["监测站"] == item]["纬度"]
                    dis_2 = geo_distance(lng1, lat1, lng_2, lat_2)  # 两站地理距离
                    if dis_2 <= 50000:  # 合并距离内的临近监测站
                        data_to_add_in_to_Iterative = pd.read_excel(input_file_path_pollution + item + ".xlsx")
                        data_to_add_in_to_Iterative = data_to_add_in_to_Iterative.set_index("日期")
                        data_to_Iterative_concat = data_to_add_in_to_Iterative[pollution_Iterative]
                        data_to_Iterative_concat = pd.DataFrame(data_to_Iterative_concat)
                        data_to_Iterative_concat.columns = [pollution_Iterative + "_add%s" % numb]
                        concat_list.append(data_to_Iterative_concat)
                        numb += 1
            if len(concat_list) > 0:  # 合并本身与临近
                data_to_Iterative = pd.concat(concat_list, axis=1, sort=False)
                data_to_Iterative = pd.concat([data_pollution[pollution_Iterative], data_to_Iterative], axis=1,
                                              sort=False)
            else:
                data_to_Iterative = data_pollution[pollution_Iterative].copy()
                data_to_Iterative = pd.DataFrame(data_to_Iterative)
                data_to_Iterative.columns = [pollution_Iterative]  # 本身
            data_pollution_Iterative_to_merge = IterativeImputer(max_iter=10).fit_transform(data_to_Iterative)
            data_pollution_Iterative_to_merge = pd.DataFrame(data_pollution_Iterative_to_merge)
            data_pollution_Iterative_to_merge = data_pollution_Iterative_to_merge.set_index(data_to_Iterative.index)
            data_pollution_Iterative_to_merge.columns = data_to_Iterative.columns
            for numb_del in range(numb):
                del data_pollution_Iterative_to_merge[pollution_Iterative + "_add%s" % numb_del]
            merge_list.append(data_pollution_Iterative_to_merge)
        data_pollution_Iterative = pd.concat(merge_list, axis=1, sort=False)

        # 对结果的0值取np.nan
        data_pollution_KNN.replace(0, np.nan, inplace=True)
        data_pollution_ewm.replace(0, np.nan, inplace=True)
        data_pollution_IDW.replace(0, np.nan, inplace=True)
        data_pollution_Iterative.replace(0, np.nan, inplace=True)

        # 合并相同方法的结果
        data_pollution_KNN = data_pollution_KNN.set_index(data_pollution.index)
        data_pollution_KNN.columns = data_pollution.columns
        data_pollution_ewm = data_pollution_ewm.set_index(data_pollution.index)
        data_pollution_ewm.columns = data_pollution.columns
        data_pollution_IDW = data_pollution_IDW.set_index(data_pollution.index)
        data_pollution_IDW.columns = data_pollution.columns
        data_pollution_Iterative = data_pollution_Iterative.set_index(data_pollution.index)
        data_pollution_Iterative.columns = data_pollution.columns

        # 合并不同方法为一个文件
        sheet_name = ["KNN", "ewm", "IDW", "Iterative"]
        sheet_name_count = 0
        writer = pd.ExcelWriter(merge_output_file_path + '%s.xlsx' % (input_file_name.replace(".xlsx", "")))
        for methods_output in [data_pollution_KNN, data_pollution_ewm, data_pollution_IDW, data_pollution_Iterative]:
            methods_output.to_excel(writer, sheet_name=sheet_name[sheet_name_count])
            sheet_name_count = 1 + sheet_name_count
        writer.save()


if __name__ == '__main__':
    print('=====主进程=====')

    p1 = Process(target=get4method, args=("样例1",))
    p2 = Process(target=get4method, args=('样例2',))
    p3 = Process(target=get4method, args=('样例3',))
    p4 = Process(target=get4method, args=('样例4',))
    p5 = Process(target=get4method, args=('样例5',))
    p6 = Process(target=get4method, args=('样例6',))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()

    p6.join()  # 依次检测是否完成, 完成才会执行join下面的代码
    p5.join()
    p4.join()
    p3.join()
    p2.join()
    p1.join()

    # 自动关机
    print("程序已完成," + str(60) + '秒后将会关机')
    print('关机')
    os.system('shutdown -s -f -t 60')
