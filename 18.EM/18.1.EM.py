# !/usr/bin/python
# -*- coding:utf-8 -*-

import numpy as np
from scipy.stats import multivariate_normal
from sklearn.mixture import GaussianMixture, GMM #GMM在0.8版本后不推荐使用，而推荐用GaussianMixture
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import pairwise_distances_argmin


mpl.rcParams['font.sans-serif'] = [u'SimHei']
mpl.rcParams['axes.unicode_minus'] = False


if __name__ == '__main__':
    style = 'myself'#自己算概率值

    np.random.seed(0)
    mu1_fact = (0, 0, 0) #构造均值
    cov1_fact = np.diag((1, 2, 3))#构造高斯分布，均值（0，0，0），方差对角线是(1, 2, 3)，其他都为0；这句构造方差
    data1 = np.random.multivariate_normal(mu1_fact, cov1_fact, 400)#使用多元高斯分布造400个样本
    mu2_fact = (2, 2, 1)
    cov2_fact = np.array(((1, 1, 3), (1, 2, 1), (0, 0, 1)))#均值(2, 2, 1)，方差无规律
    data2 = np.random.multivariate_normal(mu2_fact, cov2_fact, 100)#生成多元高斯分布，100个样本
    data = np.vstack((data1, data2))#2个样本数据叠加在一起
    y = np.array([True] * 400 + [False] * 100)#建模时使用

    if style == 'sklearn':
        g = GaussianMixture(n_components=2, covariance_type='full', tol=1e-6, max_iter=1000)#covariance_type不要求方差相同、有关联；tol容错是多少，max_iter迭代次数
        g.fit(data)#没有放入y
        print '类别概率:\t', g.weights_[0] #第一个类别占了整体数据的概率是多少
        print '均值:\n', g.means_, '\n'
        print '方差:\n', g.covariances_, '\n'
        mu1, mu2 = g.means_
        sigma1, sigma2 = g.covariances_
    else:#自己实现EM算法
        num_iter = 100
        n, d = data.shape
        # 1.随机指定
        # mu1 = np.random.standard_normal(d) #生产一个浮点数或 N 维浮点数组，取数范围：标准正态分布随机样本
        # print mu1
        # mu2 = np.random.standard_normal(d)
        # print mu2

        # 2.指定，将类别中最小值作为第一个列别的均值，最大值作为第二个类别的均值；方差取为1；-- 原因：保证可以分开，但需要多迭代几次
        mu1 = data.min(axis=0)#指定样本的mu1，mu2，sigma1，sigma2，和pi
        mu2 = data.max(axis=0)
        sigma1 = np.identity(d)# np.identity(d)：创建单位矩阵；只能获取方阵，也即标准意义的单位阵
        sigma2 = np.identity(d)
        pi = 0.5 #这里指定有2个高斯分布
        # EM
        for i in range(num_iter):
            # E Step
            norm1 = multivariate_normal(mu1, sigma1)#多元正太分布
            norm2 = multivariate_normal(mu2, sigma2)
                #np.random.multivariate_normal 方法用于根据实际情况生成一个多元正太分布矩阵
            tau1 = pi * norm1.pdf(data)#算第一个模型概率密度， norm1.pdf(data)是公式中N(xi|uk,sigma(K)) ，N(xi|uk,sigma(K))=xi*pi在i上的加和
                #整个公式中分子部分
            tau2 = (1 - pi) * norm2.pdf(data)
            gamma = tau1 / (tau1 + tau2)#表示每一个样本属于第一个类别的概率有多大, （1-gamma）即为属于第二个类别的概率有多大
            # print 'gamma的维数:',gamma.shape

            # M Step
            mu1 = np.dot(gamma, data) / np.sum(gamma) #np.dot是矩阵相乘，np.sum(gamma)是所有数据中属于第一类的概率和； np.dot(gamma, data)用来取出data中属于第一个类别的数据
            mu2 = np.dot((1 - gamma), data) / np.sum((1 - gamma))
            sigma1 = np.dot(gamma * (data - mu1).T, data - mu1) / np.sum(gamma)#gamma值乘其转置，再乘原方阵
            sigma2 = np.dot((1 - gamma) * (data - mu2).T, data - mu2) / np.sum(1 - gamma)
            pi = np.sum(gamma) / n #单纯属于每个列别的比例
            print i, ":\t", mu1, mu2#打印每轮mu值
        print '类别概率:\t', pi #纯属于第一个类别和第二个类别的比例
        print '均值:\t', mu1, mu2#打印均值
        print '方差:\n', sigma1, '\n\n', sigma2, '\n'

    # 预测分类
    norm1 = multivariate_normal(mu1, sigma1)#造的多元高斯分布模型
    norm2 = multivariate_normal(mu2, sigma2)
    tau1 = norm1.pdf(data)#算在这样的分布下，每个样本的概率密度值是什么
    tau2 = norm2.pdf(data)#tau1与tau2哪个大，取做哪个类别

    fig = plt.figure(figsize=(13, 7), facecolor='w')
    ax = fig.add_subplot(121, projection='3d')#作图
    ax.scatter(data[:, 0], data[:, 1], data[:, 2], c='b', s=30, marker='o', depthshade=True)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(u'原始数据', fontsize=18)
    ax = fig.add_subplot(122, projection='3d')
    order = pairwise_distances_argmin([mu1_fact, mu2_fact], [mu1, mu2], metric='euclidean')#欧式距离
    print order#这里输出值是[0，1],表示tau1就是第一类，如果是【1，0】，那么tau1是第二类
    if order[0] == 0:
        c1 = tau1 > tau2 #第一类
    else:
        c1 = tau1 < tau2
    c2 = ~c1
    acc = np.mean(y == c1) #均值相等了，则算对了；统计1的个数除以总个数，即为准确率
    print u'准确率：%.2f%%' % (100*acc)
    ax.scatter(data[c1, 0], data[c1, 1], data[c1, 2], c='r', s=30, marker='o', depthshade=True) #三个点的坐标
    ax.scatter(data[c2, 0], data[c2, 1], data[c2, 2], c='g', s=30, marker='^', depthshade=True)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(u'EM算法分类', fontsize=18)
    plt.suptitle(u'EM算法的实现', fontsize=21)
    plt.subplots_adjust(top=0.90)
    plt.tight_layout()
    plt.show()
