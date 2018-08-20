# -*- coding: utf-8 -*-

import xml.etree.cElementTree as et
import xml.dom.minidom as minidom
#import codecs
import os
import re
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
#用来生成包含卡口、泛卡口的list，用于detect模块，这里处理诺亚数据
srcPath='C:\\person-property-2\\10'
kakou_file=open('C:\\person-property-2\\'+'nuoya-ride-kakou.list','a+')
fankakou_file=open('C:\\person-property-2\\'+'nuoya-ride-fankakou.list','a+')
dirs = os.listdir(srcPath)#仅返回一级目录
count=0
qixing_count = 0
non_count =0
pic_num = 0
fpic_num=0
for d in dirs:
    a = d[0:-1];
    if a.endswith(".jp"):
        kakou_flag = False
        fkakou_flag = False
        if a.endswith(".jp") and os.path.exists(srcPath + a.split('.jp')[0] + '.xml'):  # xml  img 同时存在
            xmlPath = srcPath + a.split('.jp')[0] + '.xml'
            try:
                # xml = et.parse(xmlPath).getroot()
                # print(type(xml))
                xml_tree = open(xmlPath, 'r').read()  # 返回XML形式的字符串
                xml = et.XML(xml_tree)
            except:
                continue
            for object in xml.iter('Object'):  # 遍历标注目标

                try:  # sn  type 是否存在
                    sn = object.attrib['sn']  # 个数
                    type = object.attrib['type']  # 类型
                except:
                    continue

                if type == 'non-motorized': #骑行
                    qixing_count +=1
                    if object.find('PersonCyclePos') is None:
                        continue
                    fullPosition = object.find('PersonCyclePos').text
                    list = re.split(",", fullPosition)
                    x = int(list[0])
                    y = int(list[1])
                    w = int(list[2])
                    h = int(list[3])

                    # fullPosition = object.find('FullPosition')
                    # if fullPosition is None:
                    #     continue
                    # x, y, w, h = map(float, fullPosition.text.split(','))  # 赋值

                    if h >= 500:
                        count += 1
                        kakou_flag = True
                        continue
                    if h < 500:
                        non_count +=1
                        fkakou_flag = True
                        continue

                else:
                    continue
            path = srcPath + a.split('.jp')[0] + '.jpg'
            if kakou_flag :
                pic_num +=1
                kakou_file.write(path + '\n')  # 统计数据
            if fkakou_flag :
                fpic_num +=1
                fankakou_file.write(path + '\n')  # 统计数据

print qixing_count
print(count)
print non_count
print ('kakou pic number: ',pic_num)
print ('fankakou pic number: ',fpic_num)
kakou_file.close()

