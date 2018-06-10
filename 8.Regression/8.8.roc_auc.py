# -*-coding:utf-8-*-
#8.8的数据是自己造的
import numbers
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV #调参是引入这个函数
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.svm import SVC
from sklearn.preprocessing import label_binarize
from numpy import interp
from sklearn import metrics #包，算ROC曲线
from itertools import cycle


if __name__ == '__main__':
    np.random.seed(0)
    pd.set_option('display.width', 300)
    np.set_printoptions(suppress=True,linewidth=200)
    n = 300
    x = np.random.randn(n, 50)#0-1的高斯分布，n是300个
    print x.shape
    print x
    y = np.array([0]*100+[1]*100+[2]*100)#认为前100个是1个类别，中间100个是一个类别，后100个是一类；构成一个list构成一个y
    #softmax属于Logistic回归
    n_class = 3#3分类，则做3次logistic回归
#    print 'Before= \n',y

#    alpha = np.logspace(-3, 3, 7)没有使用到
    clf = LogisticRegression(penalty='l2', C=1)#用LogisticRegression，penalty指定惩罚因子，也叫正则化因子
#    GridSearchCV(clf,param_grid={C:np.logspace})#调参，param_grid={C:np.logspace}这里填内容
    clf.fit(x, y)#做梯度下降？
    y_score = clf.decision_function(x)
    print 'y_score',y_score
    y = label_binarize(y, classes=np.arange(n_class))
#    print 'After= \n', y
    colors = cycle('gbc')
    fpr = dict()
    tpr = dict()
    auc = np.empty(n_class+2)
    mpl.rcParams['font.sans-serif'] = u'SimHei'
    mpl.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(7, 6), facecolor='w')
    for i, color in zip(np.arange(n_class), colors):
        fpr[i], tpr[i], thresholds = metrics.roc_curve(y[:, i], y_score[:, i])#可算false-positive-rate和true-positive-rate
        auc[i] = metrics.auc(fpr[i], tpr[i])
        plt.plot(fpr[i], tpr[i], c=color, lw=1.5, alpha=0.7, label=u'AUC=%.3f' % auc[i])#alpha是透明度
    #这里有3个类别
    # micro
    fpr['micro'], tpr['micro'], thresholds = metrics.roc_curve(y.ravel(), y_score.ravel())#定义是micro
    auc[n_class] = metrics.auc(fpr['micro'], tpr['micro'])
    plt.plot(fpr['micro'], tpr['micro'], c='r', lw=2, ls='-', alpha=0.8, label=u'micro，AUC=%.3f' % auc[n_class])
    # macro
    fpr['macro'] = np.unique(np.concatenate([fpr[i] for i in np.arange(n_class)]))#f值做差值，已经有3条线，可以算每一点上三条线的差值，可得另外一条线
    tpr_ = np.zeros_like(fpr['macro'])
    for i in np.arange(n_class):
        tpr_ += interp(fpr['macro'], fpr[i], tpr[i])
    tpr_ /= n_class
    tpr['macro'] = tpr_
    auc[n_class+1] = metrics.auc(fpr['macro'], tpr['macro'])#算macro上fpr和tpr的值
    print auc
    print 'Macro AUC:', metrics.roc_auc_score(y, y_score, average='macro')
    plt.plot(fpr['macro'], tpr['macro'], c='m', lw=2, alpha=0.8, label=u'macro，AUC=%.3f' % auc[n_class+1])
    plt.plot((0, 1), (0, 1), c='#808080', lw=1.5, ls='--', alpha=0.7)
    plt.xlim((-0.01, 1.02))
    plt.ylim((-0.01, 1.02))
    plt.xticks(np.arange(0, 1.1, 0.1))
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.xlabel('False Positive Rate', fontsize=13)
    plt.ylabel('True Positive Rate', fontsize=13)
    plt.grid(b=True)
    plt.legend(loc='lower right', fancybox=True, framealpha=0.8, fontsize=12)
    # plt.legend(loc='lower right', fancybox=True, framealpha=0.8, edgecolor='#303030', fontsize=12)
    plt.title(u'ROC和AUC', fontsize=17)
    plt.show()


#pipeline是把若干个数据的处理过程叠在一起处理，