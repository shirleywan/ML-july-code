# -*-coding:utf-8-*-

import numpy as np
import pandas as pd
from math import sqrt

news_id = 41  # 50,82,76,115,187,
sametp_number = 3  # 同分类推荐个数
difftp_number = 2  # 不同分类推荐个数

# 读取文件
# data = pd.read_excel('C:\Users\Key\Desktop//news_features_2.xls',
#                      names=['news_Id', 'timeliness', 'reality', 'subjectivity', 'interestingness', 'hot',
#                             'fuzzification', 'type'])
data = pd.read_excel('D:\workspace//news_features.xls',
                     names=['news_Id', 'timeliness', 'reality', 'subjectivity', 'interestingness', 'hot',
                            'fuzzification', 'type'])


def produce_rec_dict(j, data):  # j:点击的news_id
    data_df = data.set_index('news_Id') #可以设置单索引和复合索引
    news_id_np = data['news_Id'].values  # news_id向量，所有的news_id值
    sum_j2 = 0
    series_j = data_df.loc[j]  # 取点击的news_id的一行（Series），点击的新闻信息
    np_j = series_j[
        ['timeliness', 'reality', 'subjectivity', 'interestingness', 'hot','fuzzification']].values
            # 取其6个特征值用于计算，type为np.ndarray
    mean_j = np_j.mean()#取平均值，所有这个news_id下的6个列别取平均值
    np_j = np_j - mean_j
    type_j_np = series_j[['type']].values
    type_j = type_j_np[0]#默认为该新闻所属第一个类别值

    for each in np_j:#所有news_id的行数据
        sum_j2 += pow(each, 2) #每个列别平方加和，MSE

    difftp_distances = []#同列别推荐列表
    sametp_distances = []#不同列别推荐列表

    i = 0
    while i < len(news_id_np):#比较所有news_id值
        if j == news_id_np[i]:
            i += 1
            continue
        else:
            compute_id = news_id_np[i]
            series_i = data_df.loc[compute_id]#取出该id的新闻信息
            type_i_np = series_i[['type']].values#找出其type
            type_i = type_i_np[0]#取其第一个列别
            dis = compute_dis(compute_id, np_j, data_df, sum_j2)#计算二者pearson相似度，sum_j2是方差
            if type_i == type_j:#如果二者类别相等，存入相同推荐列表里
                sametp_distances.append((dis, compute_id))
            else:
                difftp_distances.append((dis, compute_id))
            i += 1

    sametp_distances.sort(key=lambda x: x[0], reverse=True)#按照pearson值进行排序
    difftp_distances.sort(key=lambda x: x[0], reverse=True)
    # distance_df.to_csv('C:\Users\Key\Desktop/distance.csv', index=False)
    return sametp_distances, difftp_distances#返回两个列表


# Pearson相似度函数
def compute_dis(compute_id, np_j, data_df, sum_j2):
    sum_i2 = 0
    series_i = data_df.loc[compute_id] #取出某个news_id的所有信息
    np_i = series_i[
        ['timeliness', 'reality', 'subjectivity', 'interestingness', 'hot', 'fuzzification']].values #取出这6个值
    mean_i = np_i.mean()#取平均值
    np_i = np_i - mean_i
    numerator = np.dot(np_i.T, np_j)#平方
    for each in np_i:
        sum_i2 += pow(each, 2)
    denominator = sqrt(sum_i2) * sqrt(sum_j2)
    if denominator == 0:
        return 0
    else:
        P_dis = numerator / denominator
    return P_dis


def recommend(news_id, data, sametp_number, difftp_number):
    # 找到最近邻
    recommendations = []
    st_distance, dt_distance = produce_rec_dict(news_id, data) #计算点击的新闻id，找到近邻
    if len(st_distance) >= sametp_number:
        for k in xrange(sametp_number):
            st_nearest = st_distance[k][1]  # 返回前sametp_number个最邻近的id
            recommendations.append(st_nearest)
    if len(dt_distance) >= difftp_number:
        for l in xrange(difftp_number):
            dt_nearest = dt_distance[l][1]  # 返回前difftp_number个最邻近的id
            recommendations.append(dt_nearest)
    result = ''
    for each_id in recommendations:
        result = result + str(each_id) + ','
    return result


print recommend(news_id, data, sametp_number, difftp_number) #新闻id，全部数据data，相同分类推荐3，不同分类推荐2个；
