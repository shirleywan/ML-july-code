# -*- coding: utf-8 -*-
import xml.etree.cElementTree as et
xmlPath = "D:/dataset/person-property/3/A0510077-1_00000291.xml"

xml_tree = open(xmlPath, 'r').read()
xml = et.XML(xml_tree)

for object in xml.iter('Object'):  # 遍历标注目标
    try:  # sn  type 是否存在
        sn1 = object.attrib['sn']  # 个数
        type1 = object.attrib['type']  # 类型
    except:
        continue

    if type1 == 'non-motorized':
        # 外接框  从frame中截取patch
        # fullPosition = object.find('FullPosition')
        if (object.find('PersonCyclePos') is None) and (object.find('FullPosition') is None):
            continue
        fullPosition = ""
        if object.find('FullPosition') is not None:
            fullPosition = object.find('FullPosition').text
        if object.find('PersonCyclePos') is not None:
            fullPosition = object.find('PersonCyclePos').text
        if fullPosition is None:
            continue

        print(fullPosition)
