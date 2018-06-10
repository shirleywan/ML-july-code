# !/usr/bin/python
# -*- coding:utf-8 -*-

import numpy as np
from hmmlearn import hmm
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from sklearn.metrics.pairwise import pairwise_distances_argmin
import warnings

#若干个高斯分布之间可能有状态跳转，五角星的位置是每个高斯分布的中心
#是无监督模型，从第61行向后，没有用到label

def expand(a, b):
    return 1.05*a-0.05*b, 1.05*b-0.05*a


if __name__ == "__main__":
    warnings.filterwarnings("ignore")   # hmmlearn(0.2.0) < sklearn(0.18) #不想提示一些warning
    np.random.seed(0)

    n = 5   # 隐状态数目
    n_samples = 500
    pi = np.random.rand(n)
    pi /= pi.sum()
    print '初始概率：', pi #5个隐变量

    A = np.random.rand(n, n) #自造的转移概率
    mask = np.zeros((n, n), dtype=np.bool)
    mask[0][1] = mask[0][4] = True
    mask[1][0] = mask[1][2] = True
    mask[2][1] = mask[2][3] = True
    mask[3][2] = mask[3][4] = True
    mask[4][0] = mask[4][3] = True
    A[mask] = 0 #将true的位置清0
    for i in range(n):
        A[i] /= A[i].sum()
    print '转移概率：\n', A

    means = np.array(((30, 30, 30), (0, 50, 20), (-25, 30, 10), (-15, 0, 25), (15, 0, 40)), dtype=np.float)#均值是随便给的5个空间位置
    # means = np.random.rand(5, 3)
    print means
    for i in range(n):
        means[i,:] /= np.sqrt(np.sum(means ** 2, axis=1))[i] #均值平方和再开方
    print '均值：\n', means

    covars = np.empty((n, 3, 3))#3*3的正定矩阵
    for i in range(n):
        # covars[i] = np.diag(np.random.randint(1, 5, size=2))
        covars[i] = np.diag(np.random.rand(3)*0.02+0.001)    # np.random.rand ∈[0,1) #用来防止取到0
        #这里，0.02是方差，方差越大，数据混合的程度越大，越难以分开；而方差小会比较好分开；
        #方差的导数可以认为是精度
    print '方差：\n', covars

    model = hmm.GaussianHMM(n_components=n, covariance_type='full') #hmm中高斯hmm；n_components是5个高斯分布；covariance_type方差是完全不同的
    model.startprob_ = pi
    model.transmat_ = A
    model.means_ = means
    model.covars_ = covars
    sample, labels = model.sample(n_samples=n_samples, random_state=0)#采样，labels只有再算准确率的时候才会使用到

    # 估计参数
    model = hmm.GaussianHMM(n_components=n, covariance_type='full', n_iter=10)#建一个高斯hmm，n_iter迭代10次，
    model.fit(sample)
    y = model.predict(sample)
    np.set_printoptions(suppress=True)#保证输出的时候是小数的形式，而不是科学记数法
    print '##估计初始概率：', model.startprob_#初始概率向量
    print '##估计转移概率：\n', model.transmat_ #概率转移矩阵
    print '##估计均值：\n', model.means_ #估计的均值
    print '##估计方差：\n', model.covars_ #估计的方差
    #以上输出有加#，是因为没有做方向调整的，后面有做调整，找到最近的是谁

    # 类别
    order = pairwise_distances_argmin(means, model.means_, metric='euclidean')
    print order
    pi_hat = model.startprob_[order]
    A_hat = model.transmat_[order]
    A_hat = A_hat[:, order]
    means_hat = model.means_[order]
    covars_hat = model.covars_[order]
    change = np.empty((n, n_samples), dtype=np.bool)
    for i in range(n):
        change[i] = y == order[i]
    for i in range(n):
        y[change[i]] = i
    print '估计初始概率：', pi_hat
    print '估计转移概率：\n', A_hat
    print '估计均值：\n', means_hat
    print '估计方差：\n', covars_hat
    print labels
    print y
    acc = np.mean(labels == y) * 100
    print '准确率：%.2f%%' % acc

    mpl.rcParams['font.sans-serif'] = [u'SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    fig = plt.figure(figsize=(8, 8), facecolor='w')
    ax = fig.add_subplot(111, projection='3d')
    colors = plt.cm.Spectral(np.linspace(0,1,n))
    ax.scatter(sample[:, 0], sample[:, 1], sample[:, 2], s=50, c=labels, cmap=plt.cm.Spectral, marker='o', label=u'观测值', depthshade=True)
    plt.plot(sample[:, 0], sample[:, 1], sample[:, 2], lw=0.1, color='#A07070')
    colors = plt.cm.Spectral(np.linspace(0, 1, n))
    ax.scatter(means[:, 0], means[:, 1], means[:, 2], s=300, c=colors, edgecolor='r', linewidths=1, marker='*', label=u'中心')

    x_min, y_min, z_min = sample.min(axis=0)
    x_max, y_max, z_max = sample.max(axis=0)
    x_min, x_max = expand(x_min, x_max)
    y_min, y_max = expand(y_min, y_max)
    z_min, z_max = expand(z_min, z_max)
    ax.set_xlim((x_min, x_max))
    ax.set_ylim((y_min, y_max))
    ax.set_zlim((z_min, z_max))
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.tight_layout(1)
    plt.title(u'GMHMM参数估计和类别判定', fontsize=18)
    plt.show()
