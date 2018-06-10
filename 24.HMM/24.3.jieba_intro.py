# !/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import jieba
import jieba.posseg


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    f = open('.\\novel.txt')
    str = f.read().decode('utf-8')
    f.close()

    seg = jieba.posseg.cut(str)#也可以用jieba做cut分词，
    for word, flag in seg:
        print word, flag, '|', #这里flag表示输出词性；也可以不要词性：print word, '|',
