# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 14:13:13 2017

@author: p00355434
"""
# 分析XML文件，读取有多少个对象，计算共有多少个ped、骑行等；
# from __future__ import print_function
from PIL import Image as im

import xml.etree.cElementTree as et
import xml.dom.minidom as minidom
# import codecs
import os

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
##########################################################################################################################
### 生成标签
# savePath='D:\\HengYangLabelingData\\data\\FourkExportOut\\train\\'
# out_file=open('D:\\HengYangLabelingData\\data\\FourkExportOut\\label.txt','w')
# srcPath='D:\\Attribute-Data\\src\\FourkExportOut\\imgList.txt'
# savePath = 'D:\\dataset\\save\\'
# out_file=open('D:\\dataset\\person-property\\1\\0734a007-1\\label.txt','w+')

srcPath = 'F:\\dataset\\jfr_box\\jfr_box\\'
out_file = open('F:\\dataset\\jfr_box\\0_label.txt', 'w+')
dirs = os.listdir(srcPath)  # 仅返回一级目录
# dirs=open(srcPath,'r') #打开文件
count = 0
non_count = 0
other = 0
total_kakou = 0
total_fkakou = 0
object_num = 0
for d in dirs:

    a = d[0:-1];
    #        print(a)
    if a.endswith(".jp"):
        kakou_num = 0
        fkakou_num = 0
        # if a.endswith(".jp") :
        #     print('jpg exist')
        #
        # if (os.path.exists(srcPath+a.split('.jp')[0]+'.xml')):
        #     print('xml exist')

        if a.endswith(".jp") and os.path.exists(srcPath + a.split('.jp')[0] + '.xml'):  # xml  img 同时存在
            xmlPath = srcPath + a.split('.jp')[0] + '.xml'
            try:
                # xml = et.parse(xmlPath).getroot()
                # print(type(xml))
                xml_tree = open(xmlPath, 'r').read()  # 返回XML形式的字符串
                xml = et.XML(xml_tree)
                # tree = ET.parse("country.xml")     #打开xml文档
                ## root = ET.fromstring(country_string) #从字符串传递xml
                # root = tree.getroot()     #获得root节点
                # print root[0][1].text    # 通过下标访问
                # print root[0].tag, root[0].text
            except:
                continue

            # imgPath=srcPath+a.split('.jp')[0]+'.jpg'#第一个文件
            # # img = im.open(imgPath)
            #
            # print(imgPath) #输出文件路径
            # object_num=0

            for object in xml.iter('object'):  # 遍历标注目标
                object_num += 1
                try:  # sn  type 是否存在
                    # sn = object.attrib['sn']  # 个数
                    type = object.find('name').text  # 类型

                except:
                    continue
                if type == 'rideall' or type == 'Rideall': #骑行人
                    non_count += 1
                    continue

                if type == 'Pedestrian' or type == 'pedestrian':  # 行人
                    count = count + 1
                    # 外接框  从frame中截取patch
                    fullPosition = object.find('bndbox')

                    # fullPosition = object.find('FullPosition')

                    if fullPosition is None:
                        continue
                    # x, y, w, h = map(float, fullPosition.text.split(','))  # 赋值
                    x = int(fullPosition.find('xmin').text)
                    y = int(fullPosition.find('ymin').text)
                    w = int(fullPosition.find('xmax').text) - x
                    h = int(fullPosition.find('ymax').text) - y
                    # print(str(x) +","+str(y)+","+str(w)+","+str(h))
                    # exit(0)

                    if (h >= 500):
                        kakou_num = kakou_num + 1
                    else:
                        fkakou_num = fkakou_num + 1
                else:
                    other = other + 1
                    continue
                    #其他类型：Bus,Car,Van,Truck


        total_kakou = total_kakou + kakou_num
        total_fkakou = total_fkakou + fkakou_num

out_file.writelines('文件夹图片中有 %s 个对象' % (object_num))
out_file.write('\n')
out_file.writelines('文件夹图片中有 %s 骑行' % (non_count))
out_file.write('\n')
out_file.writelines('文件夹图片中有 %s 行人 ' % (count))
out_file.write('\n')
out_file.writelines('有%s 卡口，%s 泛卡口数据' % (total_kakou, total_fkakou))
out_file.write('\n')
out_file.writelines('文件夹图片中有 %s 个其他图片' % (other))
out_file.write('\n')
out_file.close()


##########################################################################################################################
