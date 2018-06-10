#!/usr/bin/python
# -*- coding:utf-8 -*-

import numpy as np
from sklearn import svm
from scipy import stats
from sklearn.metrics import accuracy_score
import matplotlib as mpl
import matplotlib.pyplot as plt


def extend(a, b, r):
    x = a - b
    m = (a + b) / 2
    return m-r*x/2, m+r*x/2


if __name__ == "__main__":
    np.random.seed(0)
    N = 20
    x = np.empty((4*N, 2))
    means = [(-1, 1), (1, 1), (1, -1), (-1, -1)]#数据是自造的；相当于四个象限，4个类别的均值
    sigmas = [np.eye(2), 2*np.eye(2), np.diag((1,2)), np.array(((2,1),(1,2)))]
    #1是标准高斯分布的单位矩阵，2是使其更散一点，方差更大矮胖；3更瘦长一些；4是旋转之后的；
    for i in range(4):
        mn = stats.multivariate_normal(means[i], sigmas[i]*0.3)#每个模型都随机采样采出20个样本，
        x[i*N:(i+1)*N, :] = mn.rvs(N)#放在x某个部分里
    a = np.array((0,1,2,3)).reshape((-1, 1))#y给定0123三个类别里，
    y = np.tile(a, N).flatten()#把他拉伸出来，就能造出数据
    print x
    print y
    clf = svm.SVC(C=1, kernel='rbf', gamma=1, decision_function_shape='ovo')# kernel='rbf'高斯核函数；decision_function_shape='ovo'：one-one
    # clf = svm.SVC(C=1, kernel='linear', decision_function_shape='ovr')
    #这里比较了高斯核函数和线性核函数的分类效果、准确度等等；
    clf.fit(x, y)
    y_hat = clf.predict(x)
    acc = accuracy_score(y, y_hat)
    np.set_printoptions(suppress=True)
    print u'预测正确的样本个数：%d，正确率：%.2f%%' % (round(acc*4*N), 100*acc)
    # decision_function
    #这里数据有4个类别：
    #decision_function_shape='ovo'：任意两个类别都能形成一个分类器，因此是6个分类器；返回6个值，第一个类别相对于其他分类器的距离是什么，第二个相对于其他是什么；
    #decision_function_shape='ovr'：共有4个分类器，得到的正确率基本无差别，但是模型数目少了；k个类别就有k个分类器
    print clf.decision_function(x)#关心函数返回的东西 -- 返回6个值；
    print y_hat

    x1_min, x2_min = np.min(x, axis=0)
    x1_max, x2_max = np.max(x, axis=0)
    x1_min, x1_max = extend(x1_min, x1_max, 1.05)
    x2_min, x2_max = extend(x2_min, x2_max, 1.05)
    x1, x2 = np.mgrid[x1_min:x1_max:500j, x2_min:x2_max:500j]
    x_test = np.stack((x1.flat, x2.flat), axis=1)
    y_test = clf.predict(x_test)
    y_test = y_test.reshape(x1.shape)
    cm_light = mpl.colors.ListedColormap(['#FF8080', '#A0FFA0', '#6060FF', '#F080F0'])
    cm_dark = mpl.colors.ListedColormap(['r', 'g', 'b', 'm'])
    mpl.rcParams['font.sans-serif'] = [u'SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    plt.figure(facecolor='w')
    plt.pcolormesh(x1, x2, y_test, cmap=cm_light)
    plt.scatter(x[:, 0], x[:, 1], s=40, c=y, cmap=cm_dark, alpha=0.7)
    plt.xlim((x1_min, x1_max))
    plt.ylim((x2_min, x2_max))
    plt.grid(b=True)
    plt.tight_layout(pad=2.5)
    plt.title(u'SVM多分类方法：One/One or One/Other', fontsize=18)
    plt.show()
