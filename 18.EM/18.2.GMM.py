# !/usr/bin/python
# -*- coding:utf-8 -*-

import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import train_test_split
import matplotlib as mpl
import matplotlib.colors
import matplotlib.pyplot as plt

#读取heightWeight数据，sex：0/1；height；weight。

mpl.rcParams['font.sans-serif'] = [u'SimHei']
mpl.rcParams['axes.unicode_minus'] = False
# from matplotlib.font_manager import FontProperties #读取电脑中的字体在图片中显示
# font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15)
# fontproperties=font_set


def expand(a, b):
    d = (b - a) * 0.05
    return a-d, b+d


if __name__ == '__main__':
    data = np.loadtxt('HeightWeight.csv', dtype=np.float, delimiter=',', skiprows=1)#记住这种读取方式，第一行是标题，忽略
    print data.shape#114行3列，
    y, x = np.split(data, [1, ], axis=1)#第0列是标记值，不要，因为想用无监督学习分类数据
    x, x_test, y, y_test = train_test_split(x, y, train_size=0.6, random_state=0)#随机划分训练集与测试集
    gmm = GaussianMixture(n_components=2, covariance_type='full', random_state=0)#random_state=0保证每次取的数据是一致的，默认值是null；covariance_type表明方差分布是full的
    x_min = np.min(x, axis=0)#取两个点
    x_max = np.max(x, axis=0)
    gmm.fit(x)#传入函数
    print '均值 = \n', gmm.means_#打印均值，2*2方阵，是女性身高体重/男性身高体重
    print '方差 = \n', gmm.covariances_#方差有2个矩阵，第一个是女性身高-体重的矩阵，第二个是男性的身高-体重矩阵
    y_hat = gmm.predict(x) #预测值
    y_test_hat = gmm.predict(x_test)
    change = (gmm.means_[0][0] > gmm.means_[1][0]) #boolean值，如果第一行的身高>第二行身高，表示第一行是男性数据
    #这里，如果mean的值交换了，需要将后续的标记值也交换，也就有了change；否则会有正常是男性的分类数据被标记为女性；

    if change:
        z = y_hat == 0#boolean型变量，判断值是0是1；如果是0，需要改为1
        y_hat[z] = 1#z为true的地方置1
        y_hat[~z] = 0
        z = y_test_hat == 0
        y_test_hat[z] = 1
        y_test_hat[~z] = 0

    acc = np.mean(y_hat.ravel() == y.ravel())#记录准确率
    acc_test = np.mean(y_test_hat.ravel() == y_test.ravel()) #ravel()用来将多维数组降位一维
    acc_str = u'训练集准确率：%.2f%%' % (acc * 100)
    acc_test_str = u'测试集准确率：%.2f%%' % (acc_test * 100)
    print acc_str
    print acc_test_str

    cm_light = mpl.colors.ListedColormap(['#FF8080', '#77E0A0'])
    cm_dark = mpl.colors.ListedColormap(['r', 'g'])
    x1_min, x1_max = x[:, 0].min(), x[:, 0].max()#第一列的最大值和最小值
    x2_min, x2_max = x[:, 1].min(), x[:, 1].max()#第二列的最大值和最小值
    x1_min, x1_max = expand(x1_min, x1_max)
    x2_min, x2_max = expand(x2_min, x2_max)
        # list.append(arg1) 参数类型任意，可以往已有列表中添加元素，若添加的是列表，就该列表被当成一个元素存在原列表中，只使 list 长度增加 1.
        # list.extend(list1) 参数必须是列表类型，可以将参数中的列表合并到原列表的末尾，使原来的 list 长度增加 len(list1)。
    x1, x2 = np.mgrid[x1_min:x1_max:500j, x2_min:x2_max:500j]#最大值和最小值之间产生500个数字
    grid_test = np.stack((x1.flat, x2.flat), axis=1)#将x1和x2组合起来，x1是横坐标，x2是纵坐标，共500个点
    grid_hat = gmm.predict(grid_test)#带入模型
    grid_hat = grid_hat.reshape(x1.shape)#根据x1的形状reshape
    print(grid_hat)
    if change:#第一行是男性数据 -- 将0和1转换
        z = grid_hat == 0#预测值为0，代表是第一类
        grid_hat[z] = 1 #标记为1
        grid_hat[~z] = 0
    plt.figure(figsize=(9, 7), facecolor='w')
    plt.pcolormesh(x1, x2, grid_hat, cmap=cm_light) #是预测值，也就是分类结果
    plt.scatter(x[:, 0], x[:, 1], s=50, c=y, marker='o', cmap=cm_dark, edgecolors='k') #参数s：标量或形如shape(n,)数组，可选，默认20
    plt.scatter(x_test[:, 0], x_test[:, 1], s=60, c=y_test, marker='^', cmap=cm_dark, edgecolors='k')

    p = gmm.predict_proba(grid_test)
    print p
    p = p[:, 0].reshape(x1.shape)
    CS = plt.contour(x1, x2, p, levels=(0.1, 0.5, 0.8), colors=list('rgb'), linewidths=2)
        #contour 和 contourf 都是画三维等高线图的，不同点在于 contourf 会对等高线间的区域进行填充，contour不会填充；
    plt.clabel(CS, fontsize=15, fmt='%.1f', inline=True)
    ax1_min, ax1_max, ax2_min, ax2_max = plt.axis()# plt.axis([-1, 10, 0, 6]):x轴起始于-1，终止于10，y轴起始于0，终止于6
    xx = 0.9*ax1_min + 0.1*ax1_max
    yy = 0.1*ax2_min + 0.9*ax2_max
    plt.text(xx, yy, acc_str, fontsize=18)
    yy = 0.15*ax2_min + 0.85*ax2_max
    plt.text(xx, yy, acc_test_str, fontsize=18) # plt.text：文字说明
    plt.xlim((x1_min, x1_max))
    plt.ylim((x2_min, x2_max))
    plt.xlabel(u'身高(cm)', fontsize='large')
    plt.ylabel(u'体重(kg)', fontsize='large')
    plt.title(u'EM算法估算GMM的参数', fontsize=20)
    plt.grid()
    plt.show()
