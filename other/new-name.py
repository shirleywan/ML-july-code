# -*- coding: utf-8 -*-

import xml.etree.cElementTree as et
import xml.dom.minidom as minidom
#import codecs
import os
import re
import shutil

srcPath='G:\\meiti-fankakou\\meiti_fankakou_patch1\\'
# newPath='C:\\name\\xian-22\\'
# out_file=open(newPath+'0-namelist.txt','a+')
dirs = os.listdir(srcPath)#仅返回一级目录
# b=0
# count2=0
# count1=0
for d in dirs:
    # list = d.split('0000-0000-0000-0000')
    # # print(type(list[0]))
    # new_name = list[0]+'0000-0000-0000-0000'+list[1][0:6]+"0"+list[1][7]
    # print(new_name)
    list = d.split('_')
    list[8] = "1"+list[8][1:10]
    new_name = "_".join(list)
    print(new_name)
    os.rename(srcPath+d , srcPath +new_name)


