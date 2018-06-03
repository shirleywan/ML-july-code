# !/usr/bin/python
# -*- coding:utf-8 -*-

import numpy as np
from sklearn.mixture import GaussianMixture
import scipy as sp
import matplotlib as mpl
import matplotlib.colors
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import warnings

#算似然函数，在算等高线
#概率等高线的用法：如果把概率等高线设为0.5，则超过0.5的就认为是那个类别的，如果降低等高线即可提高召回率

def expand(a, b, rate=0.05):
    d = (b - a) * rate
    return a-d, b+d


if __name__ == '__main__':
    warnings.filterwarnings(action='ignore', category=RuntimeWarning)
    np.random.seed(0)
    cov1 = np.diag((1, 2))#方差对角线为1，2，其他位置为0
    #cov=np.array(((1,0.5),(0.5,2))) #创建不同的方差，注意有3层括号
    N1 = 500
    N2 = 300
    N = N1 + N2
    x1 = np.random.multivariate_normal(mean=(3, 2), cov=cov1, size=N1)
    m = np.array(((1, 1), (1, 3)))
    x1 = x1.dot(m)
    x2 = np.random.multivariate_normal(mean=(-1, 10), cov=cov1, size=N2)
    x = np.vstack((x1, x2))
    y = np.array([0]*N1 + [1]*N2)#构成两类y值

    gmm = GaussianMixture(n_components=2, covariance_type='full', random_state=0)
    gmm.fit(x)
    centers = gmm.means_
    covs = gmm.covariances_
    print 'GMM均值 = \n', centers
    print 'GMM方差 = \n', covs
    y_hat = gmm.predict(x)

    colors = '#A0FFA0', '#E080A0',
    levels = 10
    cm = mpl.colors.ListedColormap(colors)#自定义colors颜色列表
    x1_min, x1_max = x[:, 0].min(), x[:, 0].max()
    x2_min, x2_max = x[:, 1].min(), x[:, 1].max()
    x1_min, x1_max = expand(x1_min, x1_max)
    x2_min, x2_max = expand(x2_min, x2_max)
    x1, x2 = np.mgrid[x1_min:x1_max:500j, x2_min:x2_max:500j]
    grid_test = np.stack((x1.flat, x2.flat), axis=1)
    print gmm.score_samples(grid_test) #gmm.score_samples ： Compute the weighted log probabilities for each sample.
    grid_hat = -gmm.score_samples(grid_test)
    grid_hat = grid_hat.reshape(x1.shape)
    plt.figure(figsize=(9, 7), facecolor='w')
    ax = plt.subplot(111)
    cmesh = plt.pcolormesh(x1, x2, grid_hat, cmap=plt.cm.Spectral)
    plt.colorbar(cmesh, shrink=0.9)
    CS = plt.contour(x1, x2, grid_hat, levels=np.logspace(0, 2, num=levels, base=10), colors='w', linewidths=1) #作三维等高线
    plt.clabel(CS, fontsize=9, inline=True, fmt='%.1f')
    plt.scatter(x[:, 0], x[:, 1], s=30, c=y, cmap=cm, marker='o')#画点

    for i, cc in enumerate(zip(centers, covs)):
        center, cov = cc
        value, vector = sp.linalg.eigh(cov) #计算矩阵特征向量，PCA有用到
        width, height = value[0], value[1]
        v = vector[0] / sp.linalg.norm(vector[0])#正则化
        angle = 180* np.arctan(v[1] / v[0]) / np.pi#角度
        e = Ellipse(xy=center, width=width, height=height,
                    angle=angle, color='m', alpha=0.5, clip_box = ax.bbox) #Ellipse：画椭圆；Cricle：作圆形
        ax.add_artist(e) #add_artist：添加已创建好的 artist

    plt.xlim((x1_min, x1_max))
    plt.ylim((x2_min, x2_max))
    mpl.rcParams['font.sans-serif'] = [u'SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    plt.title(u'GMM似然函数值', fontsize=20)
    plt.grid(True)
    plt.show()
