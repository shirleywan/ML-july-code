#!/usr/bin/python
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# 'sepal length', 'sepal width', 'petal length', 'petal width'
iris_feature = u'花萼长度', u'花萼宽度', u'花瓣长度', u'花瓣宽度'


if __name__ == "__main__":
    path = 'iris.data'  # 数据文件路径
    data = pd.read_csv(path, header=None)
    x, y = data[range(4)], data[4]#0,1,2,3是x，4列是y，y是个字符串
    y = pd.Categorical(y).codes#将字符串映射为0、1、2三个列别
    x = x[[0, 1]]#为了作图方便，选择第0列和第1列
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, train_size=0.6)#分成60%的训练数据，40%测试数据

    # 分类器
    clf = svm.SVC(C=0.1, kernel='linear', decision_function_shape='ovr') #做SVM的分类部分，SVC中的c是分类，支撑向量的分类器；
        # kernel='linear'：是使用线性函数，允许分类器错误率是0.1，c=0.1； decision_function_shape='ovr'：用若干个2分类得到3分类，one-vs-rest；
    # clf = svm.SVC(C=0.8, kernel='rbf', gamma=20, decision_function_shape='ovr') #kernel='rbf'高斯核函数
    clf.fit(x_train, y_train.ravel())#得到学习部分

    # 准确率
    print clf.score(x_train, y_train)  # 精度，实际训练数据和预测训练数据准确率
    print '训练集准确率：', accuracy_score(y_train, clf.predict(x_train))
    print clf.score(x_test, y_test)
    print '测试集准确率：', accuracy_score(y_test, clf.predict(x_test)) #测试数据准确率
        #2个圈的是训练数据，1个小圈的是测试数据

    # decision_function
    print x_train[:5]#只看前5个train，示例；
    #理论上，clf.decision_function(x_train)这里输入x_train,将会返回y属于那个列别；但是实际上返回的是3个数，这个点到这三个分类器的距离，那个大应该属于那个列别；包括正负号在内
    #clf.decision_function（）做预测，clf.predict(x_train)做封装；
    print 'decision_function:\n', clf.decision_function(x_train)
    print '\npredict:\n', clf.predict(x_train)

    # 画图
    x1_min, x2_min = x.min()
    x1_max, x2_max = x.max()
    x1, x2 = np.mgrid[x1_min:x1_max:500j, x2_min:x2_max:500j]  # 生成网格采样点
    grid_test = np.stack((x1.flat, x2.flat), axis=1)  # 测试点
    # print 'grid_test = \n', grid_test
    # Z = clf.decision_function(grid_test)    # 样本到决策面的距离
    # print Z
    grid_hat = clf.predict(grid_test)       # 预测分类值
    grid_hat = grid_hat.reshape(x1.shape)  # 使之与输入的形状相同
    mpl.rcParams['font.sans-serif'] = [u'SimHei']
    mpl.rcParams['axes.unicode_minus'] = False

    cm_light = mpl.colors.ListedColormap(['#A0FFA0', '#FFA0A0', '#A0A0FF'])
    cm_dark = mpl.colors.ListedColormap(['g', 'r', 'b'])
    plt.figure(facecolor='w')
    plt.pcolormesh(x1, x2, grid_hat, cmap=cm_light)
    plt.scatter(x[0], x[1], c=y, edgecolors='k', s=50, cmap=cm_dark)      # 样本
    plt.scatter(x_test[0], x_test[1], s=120, facecolors='none', zorder=10)     # 圈中测试集样本
    plt.xlabel(iris_feature[0], fontsize=13)
    plt.ylabel(iris_feature[1], fontsize=13)
    plt.xlim(x1_min, x1_max)
    plt.ylim(x2_min, x2_max)
    plt.title(u'鸢尾花SVM二特征分类', fontsize=16)
    plt.grid(b=True, ls=':')
    plt.tight_layout(pad=1.5)
    plt.show()
