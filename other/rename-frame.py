# -*- coding: utf-8 -*-

import xml.etree.cElementTree as et
import xml.dom.minidom as minidom
#import codecs
import os
import re
import shutil
if __name__=="__main__":
    srcPath='F:\\dataset\\jfr_box\\meiti_patch_kakou\\'
# newPath='C:\\name\\xian-22\\'
# out_file=open(newPath+'0-namelist.txt','a+')
    dirs = os.listdir(srcPath)#仅返回一级目录
    pic_count = ""
    frame = 0
    for d in dirs:
        name_list = d.split('_')
        num = int(name_list[3])
        if num == pic_count:
            frame +=1
            name_list[5]  = '0' * (8 - len(str(frame))) + str(frame)
        else:
            frame = 1
            name_list[5] = '0' * (8 - len(str(frame))) + str(frame)
            pic_count = num
    print name_list
    exit(0)


    os.rename(srcPath+d , srcPath +list[0]+'.png')


