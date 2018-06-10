#!/usr/bin/python
# -*- coding:utf-8 -*-
#这里是用来计算bagging的正确率的，在做n次实验中，每次正确的概率是p，
# 且只有正确的次数大于n/2时才会被认为是正确的，因此每个分类器的总正确率是n/2-n的正确率的加和；

import operator
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

#计算组合数
def c(n, k):
    return reduce(operator.mul, range(n-k+1, n+1)) / reduce(operator.mul, range(1, k+1))
'''
#补充：用来计算阶乘
def fac(n):
    return reduce(operator.mul, range(1,n+1))
'''
#计算做n次实验，每次实验正确率为p，函数用来计算n次实验总正确率
def bagging(n, p):
    s = 0
    for i in range(n / 2 + 1, n + 1):
        s += c(n, i) * p ** i * (1 - p) ** (n - i)
    #c(n, i) * p ** i * (1 - p) ** (n - i)是二项分布计算概率
    return s


if __name__ == "__main__":
    n = 100
    x = np.arange(1, n, 2)
    y = np.empty_like(x, dtype=np.float)
    #numpy.empty_like(a, dtype=None, order=’K’, subok=True)
    #a：返回值仿照的矩阵；dtype：输出的数据类型；order：‘C’ 、 ‘F’、 ‘A’、 ‘K’，表示数组在内存的存放次序是以行(C)为主还是以列(F)为主，
    # ‘A’表示以列为主存储，如果a是列相邻的，‘K’表示尽可能与a的存储方式相同；subok：bool类型，True：使用a的内部数据类型，False：使用a数组的数据类型；
    #返回值：生成与a相似（形态和数据类型）的随机矩阵；
    for i, t in enumerate(x): #enumerate函数后面跟集合时，打印出来的是元组（0，X）....0代表索引X代表元素
        y[i] = bagging(t, 0.6)
        if t % 10 == 9:
            print t, '次采样正确率：', y[i]
    mpl.rcParams[u'font.sans-serif'] = u'SimHei'
    mpl.rcParams[u'axes.unicode_minus'] = False
    plt.figure(facecolor='w')
    plt.plot(x, y, 'ro-', lw=2)
    plt.xlim(0,100) #强制绘制前100个点
    plt.ylim(0.55, 1)
    plt.xlabel(u'采样次数', fontsize=16)
    plt.ylabel(u'正确率', fontsize=16)
    plt.title(u'Bagging', fontsize=20)
    plt.grid(b=True)
    plt.show()

'''
if __name__ == "__main__":
    print c(10,2)
'''