# -*- coding: utf-8 -*-

import xml.etree.cElementTree as et
import xml.dom.minidom as minidom
#import codecs
import os
#处理媒体行人、卡口+泛卡口patch，形成list，包含：帧的名称+行人patch的坐标;

srcPath='F:\\dataset\\jfr_box\\meiti\\'
# srcPath='F:\\dataset\\jfr_box\\test\\'
# kakou_file=open('F:\\dataset\\jfr_box\\'+'ride-fankakou.list','a+')
# fkakou_file=open('F:\\dataset\\jfr_box\\'+'ride-fankakou.list','a+')
out_file = open('F:\\dataset\\jfr_box\\haisi-list.txt','a+')
dirs = os.listdir(srcPath)#仅返回一级目录
count = 0
for d in dirs:
    a = d[0:-1];
    if a.endswith(".jp"):
        if a.endswith(".jp") and os.path.exists(srcPath + a.split('.jp')[0] + '.xml'):  # xml  img 同时存在
            xmlPath = srcPath + a.split('.jp')[0] + '.xml'
            try:
                # xml = et.parse(xmlPath).getroot()
                # print(type(xml))
                xml_tree = open(xmlPath, 'r').read()  # 返回XML形式的字符串
                xml = et.XML(xml_tree)
            except:
                continue
            for object in xml.iter('object'):  # 遍历标注目标

                try:  # sn  type 是否存在
                    type = object.find('name').text  # 类型
                except:
                    continue

                if type == 'Pedestrian' or type == 'pedestrian': #骑行
                    # # 外接框  从frame中截取patch
                    # # fullPosition = object.find('Position')
                    # # fullPosition = object.find('FullPosition')
                    #
                    fullPosition = object.find('bndbox')
                    #
                    # # fullPosition = object.find('FullPosition')
                    #
                    if fullPosition is None:
                        continue
                    # x, y, w, h = map(float, fullPosition.text.split(','))  # 赋值
                    x1 = int(fullPosition.find('xmin').text)
                    y1 = int(fullPosition.find('ymin').text)
                    x2 = int(fullPosition.find('xmax').text)
                    y2 = int(fullPosition.find('ymax').text)
                    print a.split('.jp')[0] + '.jpg'+' '+str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)
                    count +=1

                    out_file.write(a.split('.jp')[0] + '.jpg'+' '+str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)+'\n')

out_file.close()
print count

