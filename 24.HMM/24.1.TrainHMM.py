# !/usr/bin/python
# -*- coding:utf-8 -*-

import math
import matplotlib.pyplot as plt
import numpy as np
import codecs
import random

#这里加入了英文词库，中文分词的效果会变差；中文的词会被分的很碎

infinite = float(-2**31)


def log_normalize(a):
    s = 0
    for x in a:
        s += x
    if s == 0:
        print "Error..from log_normalize."
        return
    s = math.log(s)
    for i in range(len(a)):
        if a[i] == 0:
            a[i] = infinite
        else:
            a[i] = math.log(a[i]) - s


def log_sum(a):
    if not a:   # a为空
        return infinite
    m = max(a)
    s = 0
    for t in a:
        s += math.exp(t-m)
    return m + math.log(s)


def calc_alpha(pi, A, B, o, alpha):
    for i in range(4):
        alpha[0][i] = pi[i] + B[i][ord(o[0])]
    T = len(o)
    temp = [0 for i in range(4)]
    del i
    for t in range(1, T):
        for i in range(4):
            for j in range(4):
                temp[j] = (alpha[t-1][j] + A[j][i])
            alpha[t][i] = log_sum(temp)
            alpha[t][i] += B[i][ord(o[t])]


def calc_beta(pi, A, B, o, beta):
    T = len(o)
    for i in range(4):
        beta[T-1][i] = 1
    temp = [0 for i in range(4)]
    del i
    for t in range(T-2, -1, -1):
        for i in range(4):
            beta[t][i] = 0
            for j in range(4):
                temp[j] = A[i][j] + B[j][ord(o[t+1])] + beta[t+1][j]
            beta[t][i] += log_sum(temp)


def calc_gamma(alpha, beta, gamma):
    for t in range(len(alpha)):
        for i in range(4):
            gamma[t][i] = alpha[t][i] + beta[t][i]
        s = log_sum(gamma[t])
        for i in range(4):
            gamma[t][i] -= s


def calc_ksi(alpha, beta, A, B, o, ksi):
    T = len(alpha)
    temp = [0 for x in range(16)]
    for t in range(T-1):
        k = 0
        for i in range(4):
            for j in range(4):
                ksi[t][i][j] = alpha[t][i] + A[i][j] + B[j][ord(o[t+1])] + beta[t+1][j]
                temp[k] =ksi[t][i][j]
                k += 1
        s = log_sum(temp)
        for i in range(4):
            for j in range(4):
                ksi[t][i][j] -= s


def bw(pi, A, B, alpha, beta, gamma, ksi, o):
    T = len(alpha)
    for i in range(4):
        pi[i] = gamma[0][i]
    s1 = [0 for x in range(T-1)]
    s2 = [0 for x in range(T-1)]
    for i in range(4):
        for j in range(4):
            for t in range(T-1):
                s1[t] = ksi[t][i][j]
                s2[t] = gamma[t][i]
            A[i][j] = log_sum(s1) - log_sum(s2)
    s1 = [0 for x in range(T)]
    s2 = [0 for x in range(T)]
    for i in range(4):
        print "bw", i
        for k in range(65536):
            valid = 0
            if k % 10000 == 0:
                print "bw - k", k
            for t in range(T):
                if ord(o[t]) == k:
                    s1[valid] = gamma[t][i]
                    valid += 1
                s2[t] = gamma[t][i]
            if valid == 0:
                B[i][k] = infinite
            else:
                B[i][k] = log_sum(s1[:valid]) - log_sum(s2)


def baum_welch(pi, A, B):
    f = file(".\\1.txt")
    sentence = f.read()[3:].decode('utf-8')
    f.close()
    T = len(sentence)
    alpha = [[0 for i in range(4)] for t in range(T)]
    beta = [[0 for i in range(4)] for t in range(T)]
    gamma = [[0 for i in range(4)] for t in range(T)]
    ksi = [[[0 for j in range(4)] for i in range(4)] for t in range(T-1)]
    for time in range(3):
        print "calc_alpha"
        calc_alpha(pi, A, B, sentence, alpha)    # alpha(t,i):给定lamda，在时刻t的状态为i且观测到o(1),o(2)...o(t)的概率
        print "calc_beta"
        calc_beta(pi, A, B, sentence, beta)      # beta(t,i)：给定lamda和时刻t的状态i，观测到o(t+1),o(t+2)...oT的概率
        print "calc_gamma"
        calc_gamma(alpha, beta, gamma)    # gamma(t,i)：给定lamda和O，在时刻t状态位于i的概率
        print "calc_ksi"
        calc_ksi(alpha, beta, A, B, sentence, ksi)    # ksi(t,i,j)：给定lamda和O，在时刻t状态位于i且在时刻i+1，状态位于j的概率
        print "bw"
        bw(pi, A, B, alpha, beta, gamma, ksi, sentence)
        print "time", time
        print "Pi:", pi
        print "A", A


def mle():  # 0B/1M/2E/3S
    pi = [0] * 4   # npi[i]：i状态的个数
    a = [[0] * 4 for x in range(4)]     # na[i][j]：从i状态到j状态的转移个数
    b = [[0]* 65536 for x in range(4)]  # nb[i][o]：从i状态到o字符的个数
    f = file(".\\pku_training.utf8")
    data = f.read()[3:].decode('utf-8')
    f.close()
    tokens = data.split('  ')
    # # 增加英文词训练集
    # f = file('Englishword.train')
    # data = f.read().decode('utf-8')
    # f.close()
    # tokens.extend(data.split(' '))

    # 开始训练，用来统计所有词的情况
    last_q = 2 #上一个词的终止位置
    iii = 0
    old_progress = 0
    print '进度：'
    for k, token in enumerate(tokens):
        progress = float(k) / float(len(tokens))
        if progress > old_progress + 0.1:
            print '%.3f%%' % (progress * 100)
            old_progress = progress
        token = token.strip()#扔掉两边空格
        n = len(token)
        if n <= 0: #如果词的长度是空的
            continue
        if n == 1:
            pi[3] += 1
            a[last_q][3] += 1   # 上一个词的结束(last_q)到当前状态(3S)
            b[3][ord(token[0])] += 1
            last_q = 3 #代表是给下一个人使用的
            continue
        # 初始向量部门
        pi[0] += 1#起始字
        pi[2] += 1#终止字
        pi[1] += (n-2)#有几个中间字
        # 转移矩阵
        a[last_q][0] += 1 #从上一个词的终止位置
        last_q = 2
        if n == 2:#begin到end
            a[0][2] += 1 #则是0-2的状态
        else:
            a[0][1] += 1#大于2，则一定是0-1，1-1，1-2的状态转移过程
            a[1][1] += (n-3) #计算1-1出现几次，类似于“天天向上”
            a[1][2] += 1
        # 发射矩阵
        b[0][ord(token[0])] += 1 #0看到0，出现一次
        b[2][ord(token[n-1])] += 1 #2-最后一个字，出现一次
        for i in range(1, n-1):
            b[1][ord(token[i])] += 1
    # 正则化，保证加和为1
    log_normalize(pi)
    for i in range(4):
        log_normalize(a[i])
        log_normalize(b[i])
    return [pi, a, b]


def list_write(f, v):
    for a in v:
        f.write(str(a))
        f.write(' ')
    f.write('\n')


def save_parameter(pi, A, B):
    f_pi = open(".\\pi.txt", "w")
    list_write(f_pi, pi)
    f_pi.close()
    f_A = open(".\\A.txt", "w")
    for a in A:
        list_write(f_A, a)
    f_A.close()
    f_B = open(".\\B.txt", "w")
    for b in B:
        list_write(f_B, b)
    f_B.close()


if __name__ == "__main__":
    pi, A, B = mle()
    save_parameter(pi, A, B) #存下3个参数
    print "训练完成..."
