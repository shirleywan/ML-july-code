#!/usr/bin/python
# -*- coding:utf-8 -*-

# 导入NumPy函数库，一般都是用这样的形式(包括别名np，几乎是约定俗成的)
import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import time
from scipy.optimize import leastsq
from scipy import stats
import scipy.optimize as opt
import matplotlib.pyplot as plt
from scipy.stats import norm, poisson
# from scipy.interpolate import BarycentricInterpolator
# from scipy.interpolate import CubicSpline
import math
# import seaborn


def residual(t, x, y):
    return y - (t[0] * x ** 2 + t[1] * x + t[2])


def residual2(t, x, y):
    print t[0], t[1]
    return y - (t[0]*np.sin(t[1]*x) + t[2])


# x ** x        x > 0
# (-x) ** (-x)  x < 0
def f(x):  #0的0次方是1
    y = np.ones_like(x)
    i = x > 0
    y[i] = np.power(x[i], x[i])
    i = x < 0
    y[i] = np.power(-x[i], -x[i])
    return y


if __name__ == "__main__":
    # # 开场白：
    # numpy是非常好用的数据包，如：可以这样得到这个二维数组
    # [[ 0  1  2  3  4  5]
    #  [10 11 12 13 14 15]
    #  [20 21 22 23 24 25]
    #  [30 31 32 33 34 35]
    #  [40 41 42 43 44 45]
    #  [50 51 52 53 54 55]]
    # a = np.arange(0, 60, 10).reshape((-1, 1)) + np.arange(6)
    # print a

    # 正式开始  -:)
    # 标准Python的列表(list)中，元素本质是对象。
    # 如：L = [1, 2, 3]，需要3个指针和三个整数对象，对于数值运算比较浪费内存和CPU。
    # 因此，Numpy提供了ndarray(N-dimensional array object)对象：存储单一数据类型的多维数组。

    # # 1.使用array创建
    # 通过array函数传递list对象
    # L = [1, 2, 3, 4, 5, 6]
    # # print "L = ", L
    # a = np.array(L)
    # print "a = ", a
    # # print type(a), type(L)
    # # 若传递的是多层嵌套的list，将创建多维数组
    # b = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    # print b
    # # # #
    # # # # # 数组大小可以通过其shape属性获得
    # print a.shape
    # print b.shape
    # # # #
    # # # # 也可以强制修改shape
    # # b.shape = 4, 3
    # # print b
    # # # # # 注：从(3,4)改为(4,3)并不是对数组进行转置，而只是改变每个轴的大小，数组元素在内存中的位置并没有改变
    # # # #
    # # # 当某个轴为-1时，将根据数组元素的个数自动计算此轴的长度
    # b.shape = 2, -1
    # print b
    # print b.shape
    # # # #
    # b.shape = 3, 4
    # print b
    # # # # 使用reshape方法，可以创建改变了尺寸的新数组，原数组的shape保持不变
    # c = b.reshape((4, -1))
    # print "b = \n", b
    # print 'c = \n', c
    # # #
    # # # # 数组b和c共享内存，修改任意一个将影响另外一个
    # b[0][1] = 20
    # print "b = \n", b
    # print "c = \n", c
    # # # #
    # # # # 数组的元素类型可以通过dtype属性获得
    # print a.dtype
    # print b.dtype
    # # # #
    # # # # # 可以通过dtype参数在创建时指定元素类型
    # d = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], dtype=np.float)
    # # f = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], dtype=np.complex)
    # print d
    # print f
    # # #
    # # # 如果更改元素类型，可以使用astype安全的转换
    # f = d.astype(np.int)
    # print f
    # #
    # # # 但不要强制仅修改元素类型，如下面这句，将会以int来解释单精度float类型
    # d.dtype = np.int
    # print d
    #
    # 2.使用函数创建
    # 如果生成一定规则的数据，可以使用NumPy提供的专门函数
    # arange函数类似于python的range函数：指定起始值、终止值和步长来创建数组
    # 和Python的range类似，arange同样不包括终值；但arange可以生成浮点类型，而range只能是整数类型
    # a = np.arange(1, 10, 0.5)
    # print a
    # # # #
    # # # # linspace函数通过指定起始值、终止值和元素个数来创建数组，缺省包括终止值
    # b = np.linspace(1, 10, 10) 
    # print 'b = ', b
    # # # #
    # # 可以通过endpoint关键字指定是否包括终值
    # c = np.linspace(1, 10, 10, endpoint=False)
    # print 'c = ', c
    # # # #
    # # # 和linspace类似，logspace可以创建等比数列
    # # 下面函数创建起始值为10^1，终止值为10^2，有10个数的等比数列
    # d = np.logspace(1, 2, 9, endpoint=True)
    # print d
    # # # #
    # # # # 下面创建起始值为2^0，终止值为2^10(包括)，有10个数的等比数列
    # f = np.logspace(0, 10, 11, endpoint=True, base=2)
    # print f
    # # # #
    # # # # 使用 frombuffer, fromstring, fromfile等函数可以从字节序列创建数组
    # s = 'abcdz' #aciss码转换成int8的形式
    # g = np.fromstring(s, dtype=np.int8)
    # print g
    # #
    
    
    # 3.存取
    # 3.1常规办法：数组元素的存取方法和Python的标准方法相同
    # a = np.arange(10)
    # print a
    # # # 获取某个元素
    # print a[3]
    # # # # # 切片[3,6)，左闭右开 不包含6
    # print a[3:6]
    # # 省略开始下标，表示从0开始，且不包含5
    # print a[:5]
    # # 下标为负表示从后向前数，直到9
    # print a[3:]
    # # 步长为2
    # print a[1:9:2] #输出1，3，5，7
    # # # # # 步长为-1，即翻转
    # print a[::-1] #输出987654321
    # # # # # 切片数据是原数组的一个视图，与原数组共享内容空间，可以直接修改元素值
    # a[1:4] = 10, 20, 30 #将a数组中第1，2，3位改成10，20，30
    # print a  #输出0，10，20，30，4，5，6，7，8，9
    # # 因此，在实践中，切实注意原始数据是否被破坏，如：
    # b = a[2:5] #b=2，3，4
    # b[0] = 200 #b=200，3，4
    # print a #a=0，1，200，3，4，5，6，7，8，9

    # 3.2 整数/布尔数组存取
    # 3.2.1
    # 根据整数数组存取：当使用整数序列对数组元素进行存取时，
    # 将使用整数序列中的每个元素作为下标，整数序列可以是列表(list)或者数组(ndarray)。
    # 使用整数序列作为下标获得的数组不和原始数组共享数据空间。
    # a = np.logspace(0, 9, 10, base=2) #2的0次方-2^9；取10个值
    # print a
    #【1，2，4，8，16，31，64，128，256，512】
    # i = np.arange(0, 10, 2) #步长是2
    # print i
    # # 利用i取a中的元素
    # b = a[i]
    # print b
    # # b的元素更改，a中元素不受影响，因为b是从a中取出来的，已经取出，不是赋值
    # b[2] = 1.6
    # print b
    # print a

    # # 3.2.2
    # 使用布尔数组i作为下标存取数组a中的元素：返回数组a中所有在数组b中对应下标为True的元素
    # 生成10个满足[0,1)中均匀分布的随机数
    # a = np.random.rand(10) #rand（）生成0-1的随机数；函数中默认值是1，只生成1个数字，给10，生成10个
    # print a
    # # 大于0.5的元素索引
    # print a > 0.5 #得到boolean数组
    # # 大于0.5的元素
    # b = a[a > 0.5] #用boolean数组取出原始数组中为true的数据
    # print b
    # # 将原数组中大于0.5的元素截取成0.5
    # a[a > 0.5] = 0.5 #把数组中大于0.5的数据强制转换为0.5
    # print a
    # # # # b不受影响
    # print b

    # 3.3 二维数组的切片
    # [[ 0  1  2  3  4  5]
    #  [10 11 12 13 14 15]
    #  [20 21 22 23 24 25]
    #  [30 31 32 33 34 35]
    #  [40 41 42 43 44 45]
    #  [50 51 52 53 54 55]]
    # a = np.arange(0, 60, 10)    # 行向量
    # print 'a = ', a  #【0 10 20 30 40 50】
    # b = a.reshape((-1, 1))      # 转换成列向量
    # print b
    # c = np.arange(6) #【0 1 2 3 4 5】 不包含6 步长为1
    # print c
    # f = b + c   # 行 + 列，6*6的矩阵【0 1 2 3 4 5；10 11 12 13 14 15 ...】
    # print f
    # # 合并上述代码：
    # a = np.arange(0, 60, 10).reshape((-1, 1)) + np.arange(6) #合并后的结果
    # print a
    # # 二维数组的切片
    # print a[[0, 1, 2], [2, 3, 4]]#取出（0，2）（1，3）（2，4），构成一个新数组
    # print a[4, [2, 3, 4]] #第一个4代表第一个维度要第四行的，第二个维度要2-4，所以输出【42 43 44】
    # print a[4:, [2, 3, 4]] #4:从4行还是后面所有的行都要，输出【42 43 44，52 53 54】
    # i = np.array([True, False, True, False, False, True]) #行数上留0，2，5行
    # print a[i] #输出这三行
    # print a[i, 3] #只留这三行的第四列

    # 4.1 numpy与Python数学库的时间比较
    # for j in np.logspace(0, 7, 10):
    #     j = int(j)
    #     x = np.linspace(0, 10, j)
    #     start = time.clock()
    #     y = np.sin(x)
    #     t1 = time.clock() - start
    #
    #只计算1次，将以上代码修改为：
        N=1000
        x = np.linspace(0, 10, N)
        start = time.clock()
        y = np.sin(x)
        t1 = time.clock() - start  #结果：numpy更快
    #与下面math包中的sin（）函数比较运算时间：
    #     x = x.tolist()
    #     start = time.clock()
    #     for i, t in enumerate(x):
    #         x[i] = math.sin(t)
    #     t2 = time.clock() - start
    #     print j, ": ", t1, t2, t2/t1


    # 4.2 元素去重
    # 4.2.1直接使用库函数
    # a = np.array((1, 2, 3, 4, 5, 5, 7, 3, 2, 2, 8, 8))
    # print '原始数组：', a
    # # # 使用库函数unique ---- 元素去重
    # b = np.unique(a)  
    # print '去重后：', b  #【1 2 3 4 5 7 8】
    # # # 4.2.2 二维数组的去重，结果会是预期的么？
    # c = np.array(((1, 2), (3, 4), (5, 6), (1, 3), (3, 4), (7, 6))) 
    # print u'二维数组：\n', c  
    # print '去重后：', np.unique(c) #输出：【1 2 3 4 5 6 7】，会将c转换为一维数组
    
    
    # # # 4.2.3 方案1：转换为虚数
    # # r, i = np.split(c, (1, ), axis=1)
    # # x = r + i * 1j
    # x = c[:, 0] + c[:, 1] * 1j #c[:, 0]：表示所有的行都要，选中第一列，也就是所有二维数组的第一列； c[:, 1]选中第二列
    # print '转换成虚数：', x
    # print '虚数去重后：', np.unique(x)
    # print np.unique(x, return_index=True)   # 思考return_index的意义，索引值代表原数据所在位置，无重复元素的下标
    # idx = np.unique(x, return_index=True)[1]
    # print '二维数组去重：\n', c[idx]
    
    # # 4.2.3 方案2：利用set
    # print '去重方案2：\n', np.array(list(set([tuple(t) for t in c]))) #c是整个数组，t是从c中拿出来的每一个元素，转为tuple，放到list中，转为array，通过数据结构的转换实现去重

    # 4.3 stack and axis
    # a = np.arange(1, 10).reshape((3, 3))
    # b = np.arange(11, 20).reshape((3, 3))
    # c = np.arange(101, 110).reshape((3, 3))
    # print 'a = \n', a
    # print 'b = \n', b
    # print 'c = \n', c
    # print 'axis = 0 \n', np.stack((a, b, c), axis=0) #stack实现3个数组的堆叠；axis是旋转的轴，0-整个数组是0号轴，1-第一行，2-元素；abc的整个数组堆在一起
    # print 'axis = 1 \n', np.stack((a, b, c), axis=1) #分别取3个数组的第一行、第二行、第三行堆在一起
    # print 'axis = 2 \n', np.stack((a, b, c), axis=2) #分别取abc（0，0）形成第一行、（0，1）形成第二行，（0，2）第三行
    #stack在后续图片处理上使用更多

    # a = np.arange(1, 10).reshape(3,3)
    # print a
    # b = a + 10 #a中每一个元素都加10
    # print b
    # print np.dot(a, b) #dot：正常的矩阵乘法；1*11+2*14+3*17=90；1*12+2*15+3*18=96
    # print a * b #这种写法表示对应元素相乘。1*11；2*12；3*13

    # a = np.arange(1, 10)
    # print a
    # b = np.arange(20,25)
    # print b
    # print np.concatenate((a, b)) #连接：【123456789】+【20 21 22 23 24】=【123456789 20 21 22 23 24】
    #numpy底层是c实现，最省空间的方法是：先申请一个栈，在向里面加元素
    
    # 5.绘图
    # 5.1 绘制正态分布概率密度函数
    mpl.rcParams['font.sans-serif'] = [u'SimHei']  #FangSong/黑体 FangSong/KaiTi，指定字体，即可输出汉字
    mpl.rcParams['axes.unicode_minus'] = False #默认unicode编码，这个选false
    mu = 0 #均值
    sigma = 1 #方差
    x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 51) #等差数列取51个包含断点；
    y = np.exp(-(x - mu) ** 2 / (2 * sigma ** 2)) / (math.sqrt(2 * math.pi) * sigma) #正态分布公式
    print x.shape
    print 'x = \n', x
    print y.shape
    print 'y = \n', y
    # plt.plot(x, y, 'ro-', linewidth=2)
    plt.figure(facecolor='w') #matplotlib的简写为plt，这句表示图片默认背景是白色
    plt.plot(x, y, 'r-', x, y, 'go', linewidth=2, markersize=8) #'r-'表示红色实线，'go'表示绿色圆圈，linewidth=2线的宽度是2，markersize=8大小是8
    #plt.plot(x, y, 'ro-', linewidth=2, markersize=8) #红色的线和圈
    plt.xlabel('X', fontsize=15) #x轴标记，字号15
    plt.ylabel('Y', fontsize=15)
    plt.title(u'高斯分布函数', fontsize=18) #title，字符18，u'高斯分布函数'：为了输出汉字，u是utf-8
    plt.grid(True) #边界为true
    plt.show()

    # # 5.2 损失函数：Logistic损失(-1,1)/SVM Hinge损失/ 0/1损失
    #plt.figure(figsize=(10,8)) #指定图片大小，宽10英寸，高8英寸，（1000*800）不小了
    # x = np.array(np.linspace(start=-2, stop=3, num=1001, dtype=np.float))
        ## x = np.linspace(start=-2, stop=3, num=1001, dtype=np.float) #这样写即可
    # y_logit = np.log(1 + np.exp(-x)) / math.log(2) #除系数是为了保证图像经过（0，1），logistic回归公式：1+e^(-x)
    # y_boost = np.exp(-x) #提升
    # y_01 = x < 0 #0-1损失，x<0时y=1，x>0时y=0：只要x小于0，y即为true，x大于0，y是false
    # y_hinge = 1.0 - x #SVM中的hinge损失，y值只要比0小强制截成0，
    # y_hinge[y_hinge < 0] = 0 #把小于0的部分强制清0
    # plt.plot(x, y_logit, 'r-', label='Logistic Loss', linewidth=2)
    # plt.plot(x, y_01, 'g-', label='0/1 Loss', linewidth=2)
    # plt.plot(x, y_hinge, 'b-', label='Hinge Loss', linewidth=2)
    # # plt.plot(x, y_boost, 'm--', label='Adaboost Loss', linewidth=2)
    # plt.grid()
    # plt.legend(loc='upper right') #图例放在什么位置，图例--每条线的说明
    # # plt.savefig('1.png') #运行时保存图片，图片名是1.png
    # plt.show() #画出各种线

    # 5.3 x^x
    # x = np.linspace(-1.3, 1.3, 101) #x的取值，-1.3-1.3，取101个，则包含0，则x是个101维的向量
    # y = f(x) #f(x)定义在上面 
    # plt.figure(facecolor='w')
    # plt.plot(x, y, 'g-', label='x^x', linewidth=2)
    # plt.grid()
    # plt.legend(loc='upper left')
    # plt.show()

    #根据上例5.3可知，函数先减后增，在e^(-1)处取得极值
    
    # # 5.4 胸型线
    # x = np.arange(1, 0, -0.001)
    # y = (-3 * x * np.log(x) + np.exp(-(40 * (x - 1 / np.e)) ** 4) / 25) / 2 #np.exp(-(40 * (x - 1 / np.e)) ** 4这部分是个微小扰动
    # plt.figure(figsize=(5,7), facecolor='w')
    # plt.plot(y, x, 'r-', linewidth=2)
    # plt.grid(True)
    # plt.title(u'胸型线', fontsize=20)
    # # plt.savefig('breast.png')
    # plt.show()

    # 5.5 心形线
    # t = np.linspace(0, 2*np.pi, 100)
    # x = 16 * np.sin(t) ** 3
    # y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
    # plt.plot(x, y, 'r-', linewidth=2)
    # plt.grid(True)
    # plt.show()

    # # 5.6 渐开线  
        #中心位置可取圆或正方形，做渐开线
    # t = np.linspace(0, 50, num=1000)
    # x = t*np.sin(t) + np.cos(t)
    # y = np.sin(t) - t*np.cos(t)
    # plt.plot(x, y, 'r-', linewidth=2)
    # plt.grid()
    # plt.show()

    # # Bar
    # x = np.arange(0, 10, 0.1)
    # y = np.sin(x)
    # plt.bar(x, y, width=0.04, linewidth=0.2)
    # plt.plot(x, y, 'r--', linewidth=2)
    # plt.title(u'Sin曲线')
    # plt.xticks(rotation=-60)
    # plt.xlabel('X')
    # plt.ylabel('Y')
    # plt.grid()
    # plt.show()

    # # 6. 概率分布
    # # 6.1 均匀分布
    # x = np.random.rand(10000)
    # t = np.arange(len(x))
    # plt.hist(x, 30, color='m', alpha=0.5, label=u'均匀分布') #hist做直方图，x是基础值，30是取30份，颜色，alpha表示透不透明，0透明，1不透明
    # # plt.plot(t, x, 'r-', label=u'均匀分布')
    # plt.plot(t, x, 'g.', label=u'均匀分布') #用绿色的点显示
    # plt.legend(loc='upper left')
    # plt.grid()
    # plt.show()

    # # 6.2 验证中心极限定理
    # t = 1000
    # a = np.zeros(10000)
    # for i in range(t):
    #     a += np.random.uniform(-5, 5, 10000) #uniform：从-5到5做均匀分布，取10000个
    # a /= t
    # plt.hist(a, bins=30, color='g', alpha=0.5, normed=True, label=u'均匀分布叠加') #多个均匀分布的叠加，实质上就是gauss分布
    # plt.legend(loc='upper left')
    # plt.grid()
    # plt.show()

    # 6.21 其他分布的中心极限定理
    # 泊松分布累加验证中心极限定理
    # lamda = 10 #随机取的值
    # p = stats.poisson(lamda) #poisson分布；
    # y = p.rvs(size=1000) #rvs：random value 随机离散的值，在里面采样，取1000个。y就是泊松分布
    # mx = 30 #取30个做直方图
    # r = (0, mx)
    # bins = r[1] - r[0]
    # plt.figure(figsize=(10, 8), facecolor='w')
    # plt.subplot(121) #121：做1行2类的图，画第1个图，是图片的切割
    # plt.hist(y, bins=bins, range=r, color='g', alpha=0.8, normed=True) #y值，30个类别，range=r：范围，normed=True规则化一下，不要次数而是频率；range=r这样写是满足改前面即可。  #泊松分布做的直方图
    # t = np.arange(0, mx+1)
    # plt.plot(t, p.pmf(t), 'ro-', lw=2) # p.pmf(t)：p是lamda=10的泊松分布的概率质量函数，是真正的概率质量函数，是线
    # plt.grid(True)
    #
    # N = 1000 
    # M = 10000 #每次里面做多少次采样
    # plt.subplot(122) #第2张图
    # a = np.zeros(M, dtype=np.float) #
    # p = stats.poisson(lamda) #建模好的泊松分布，后续做累加
    # for i in np.arange(N):
    #     y = p.rvs(size=M) #泊松分布做采样，采m次样
    #     a += y #累加给a ，化简：a += p.rvs(size=M)
    # a /= N
    # plt.hist(a, bins=20, color='g', alpha=0.8, normed=True)
    # plt.grid(b=True)
    # plt.show()

    # # 6.3 Poisson分布
    # x = np.random.poisson(lam=5, size=10000)
    # print x
    # pillar = 15
    # a = plt.hist(x, bins=pillar, normed=True, range=[0, pillar], color='g', alpha=0.5) #a是y值+x值，表示每个x下y的值
    # plt.grid()
    # # plt.show()
    # print a
    # print a[0].sum() #y的加和是1

    # # 6.4 直方图的使用
    # mu = 2
    # sigma = 3
    # data = mu + sigma * np.random.randn(1000) #
    # h = plt.hist(data, 30, normed=1, color='g') #颜色可以自己调，‘#FFA0FF’-RGB的大小
    # x = h[1]
    # y = norm.pdf(x, loc=mu, scale=sigma)
    # plt.plot(x, y, 'r--', x, y, 'ro', linewidth=2, markersize=4)
    # plt.grid()
    # plt.show()


    # # 6.5 插值
    # 先做泊松分布，在求概率密度函数，再做各种插值
    # rv = poisson(5)
    # x1 = a[1]
    # y1 = rv.pmf(x1)
    # itp = BarycentricInterpolator(x1, y1)  # 重心插值
    # x2 = np.linspace(x.min(), x.max(), 50)
    # y2 = itp(x2)
    # cs = scipy.interpolate.CubicSpline(x1, y1)       # 三次样条插值
    # plt.plot(x2, cs(x2), 'm--', linewidth=5, label='CubicSpine')           # 三次样条插值
    # plt.plot(x2, y2, 'g-', linewidth=3, label='BarycentricInterpolator')   # 重心插值
    # plt.plot(x1, y1, 'r-', linewidth=1, label='Actural Value')             # 原始值
    # plt.legend(loc='upper right')
    # plt.grid()
    # plt.show()

    # 7. 绘制三维图像
    
    #简单函数：
    x, y = np.ogrid[-3:3:7j, -3:3:7j] #ogrid是取1行或1列，mgrid:表示做拼接，表示x和y的坐标；要找资料，课程是2：16：00
    print x
    print y
    
    #meshgrid与mgrid：结论相同
    
    # x, y = np.ogrid[-3:3:100j, -3:3:100j] #100j：取100个
    # # u = np.linspace(-3, 3, 101)
    # # x, y = np.meshgrid(u, u)
    # z = x*y*np.exp(-(x**2 + y**2)/2) / math.sqrt(2*math.pi) #2元正态分布
    # # z = x*y*np.exp(-(x**2 + y**2)/2) / math.sqrt(2*math.pi)
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # # ax.plot_surface(x, y, z, rstride=5, cstride=5, cmap=cm.coolwarm, linewidth=0.1)  #
    # ax.plot_surface(x, y, z, rstride=5, cstride=5, cmap=cm.Accent, linewidth=0.5) #画个曲面
    # plt.show()
    # # cmaps = [('Perceptually Uniform Sequential',
    # #           ['viridis', 'inferno', 'plasma', 'magma']),
    # #          ('Sequential', ['Blues', 'BuGn', 'BuPu',
    # #                          'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd',
    # #                          'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu',
    # #                          'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd']),
    # #          ('Sequential (2)', ['afmhot', 'autumn', 'bone', 'cool',
    # #                              'copper', 'gist_heat', 'gray', 'hot',
    # #                              'pink', 'spring', 'summer', 'winter']),
    # #          ('Diverging', ['BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr',
    # #                         'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral',
    # #                         'seismic']),
    # #          ('Qualitative', ['Accent', 'Dark2', 'Paired', 'Pastel1',
    # #                           'Pastel2', 'Set1', 'Set2', 'Set3']),
    # #          ('Miscellaneous', ['gist_earth', 'terrain', 'ocean', 'gist_stern',
    # #                             'brg', 'CMRmap', 'cubehelix',
    # #                             'gnuplot', 'gnuplot2', 'gist_ncar',
    # #                             'nipy_spectral', 'jet', 'rainbow',
    # #                             'gist_rainbow', 'hsv', 'flag', 'prism'])]

    # 8.1 scipy
    # 线性回归例1
    # x = np.linspace(-2, 2, 50)
    # A, B, C = 2, 3, -1
    # y = (A * x ** 2 + B * x + C) + np.random.rand(len(x))*0.75
    #
    # t = leastsq(residual, [0, 0, 0], args=(x, y))
    # theta = t[0]
    # print '真实值：', A, B, C
    # print '预测值：', theta
    # y_hat = theta[0] * x ** 2 + theta[1] * x + theta[2]
    # plt.plot(x, y, 'r-', linewidth=2, label=u'Actual')
    # plt.plot(x, y_hat, 'g-', linewidth=2, label=u'Predict')
    # plt.legend(loc='upper left')
    # plt.grid()
    # plt.show()

    # # 线性回归例2
    # x = np.linspace(0, 5, 100)
    # a = 5
    # w = 1.5
    # phi = -2
    # y = a * np.sin(w*x) + phi + np.random.rand(len(x))*0.5
    #
    # t = leastsq(residual2, [3, 5, 1], args=(x, y))
    # theta = t[0]
    # print '真实值：', a, w, phi
    # print '预测值：', theta
    # y_hat = theta[0] * np.sin(theta[1] * x) + theta[2]
    # plt.plot(x, y, 'r-', linewidth=2, label='Actual')
    # plt.plot(x, y_hat, 'g-', linewidth=2, label='Predict')
    # plt.legend(loc='lower left')
    # plt.grid()
    # plt.show()

    # # 8.2 使用scipy计算函数极值
    # a = opt.fmin(f, 1)
    # b = opt.fmin_cg(f, 1)
    # c = opt.fmin_bfgs(f, 1)
    # print a, 1/a, math.e
    # print b
    # print c

    # marker	description
    # ”.”	point
    # ”,”	pixel
    # “o”	circle
    # “v”	triangle_down
    # “^”	triangle_up
    # “<”	triangle_left
    # “>”	triangle_right
    # “1”	tri_down
    # “2”	tri_up
    # “3”	tri_left
    # “4”	tri_right
    # “8”	octagon
    # “s”	square
    # “p”	pentagon
    # “*”	star
    # “h”	hexagon1
    # “H”	hexagon2
    # “+”	plus
    # “x”	x
    # “D”	diamond
    # “d”	thin_diamond
    # “|”	vline
    # “_”	hline
    # TICKLEFT	tickleft
    # TICKRIGHT	tickright
    # TICKUP	tickup
    # TICKDOWN	tickdown
    # CARETLEFT	caretleft
    # CARETRIGHT	caretright
    # CARETUP	caretup
    # CARETDOWN	caretdown