#!/usr/bin/python
# -*- coding:utf-8 -*-

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso, Ridge
from sklearn.model_selection import GridSearchCV#交叉验证


if __name__ == "__main__":
    # pandas读入
    data = pd.read_csv('Advertising.csv')    # TV、Radio、Newspaper、Sales
    x = data[['TV', 'Radio', 'Newspaper']]
    # x = data[['TV', 'Radio']]
    y = data['Sales']
    print x
    print y

    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)
    #train_test_split(x, y, random_state=1,train_size=0.8) 80%是训练数据，20%是测试数据;train_size=100,100条训练数据
    #与train_size=0.8对应的是：test_sizerandom_shuffle
    # model = Lasso()
    model = Ridge()
    alpha_can = np.logspace(-3, 2, 10)#0.001-100，等比均匀取10个数字
    np.set_printoptions(suppress=True)#指定numpy的输出不是科学记数法的方式输出，而是以正常的小数方式输出的，默认suppress为false
    print 'alpha_can = ', alpha_can
    lasso_model = GridSearchCV(model, param_grid={'alpha': alpha_can}, cv=5)#5折交叉验证
    lasso_model.fit(x_train, y_train)
    print '超参数：\n', lasso_model.best_params_

    order = y_test.argsort(axis=0) #把y的测试数据y_test做递增，argsort函数使数据位置标号与数据值做对应，数据值排序后x可以对应到y的位置
#    print order #order显示出：58-39；40-22等等，数据值58在第39位...
    y_test = y_test.values[order] #用order重新选择y值
    x_test = x_test.values[order, :] #确定新的x值
    #以上三行是为了作图方便而做的排序，
    y_hat = lasso_model.predict(x_test)#x_test是测试数据，带入模型
    print lasso_model.score(x_test, y_test) #score函数是计算r方的模型，小于1越接近1越好
    mse = np.average((y_hat - np.array(y_test)) ** 2)  # Mean Squared Error，均方误差
    rmse = np.sqrt(mse)  # Root Mean Squared Error
    print mse, rmse

    t = np.arange(len(x_test))
    mpl.rcParams['font.sans-serif'] = [u'simHei']
    mpl.rcParams['axes.unicode_minus'] = False
    plt.figure(facecolor='w')
    plt.plot(t, y_test, 'r-', linewidth=2, label=u'真实数据')
    plt.plot(t, y_hat, 'g-', linewidth=2, label=u'预测数据')
    plt.title(u'线性回归预测销量', fontsize=18)
    plt.legend(loc='upper right')
    plt.grid()
    plt.show()
