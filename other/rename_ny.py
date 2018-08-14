# -*- coding: utf-8 -*-
import os
from PIL import Image as im
import xml.etree.cElementTree as et
import datetime
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import shutil
from textwrap import wrap
import xml.dom.minidom as minidom
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
#骑行图片的截取，也分为卡口、泛卡口；
#诺亚的骑行overlap

def mat_inter(box1, box2):
    # 判断两个矩形是否相交
    # box=(xA,yA,xB,yB)
    x01, y01, x02, y02 = box1
    x11, y11, x12, y12 = box2

    lx = abs((x01 + x02) / 2 - (x11 + x12) / 2)
    ly = abs((y01 + y02) / 2 - (y11 + y12) / 2)
    sax = abs(x01 - x02)
    sbx = abs(x11 - x12)
    say = abs(y01 - y02)
    sby = abs(y11 - y12)
    if lx <= (sax + sbx) / 2 and ly <= (say + sby) / 2:
        return True
    else:
        return False


def solve_coincide(box1, box2):
    # box=[xA,yA,xB,yB]
    # 计算两个矩形框的重合度
        x01, y01, x02, y02 = box1
        x11, y11, x12, y12 = box2
        col = min(x02, x12) - max(x01, x11)
        row = min(y02, y12) - max(y01, y11)
        intersection = col * row

        area1 = (x02 - x01) * (y02 - y01)
        area2 = (x12 - x11) * (y12 - y11)
        # coincide = float(intersection / (area1 + area2 - intersection))
        coincide=format(float(intersection) / float((area1 + area2 - intersection)), '.5f') #保留5位小数
        return coincide

def suit(box1,box2):
    if solve_coincide(box1,box2) > 0.6:
        return True
    return False

def contains(box1,box2):
    x01, y01, x02, y02 = box1
    x11, y11, x12, y12 = box2
    if(x01 <= x11 and x11 <= x02 and x12 <= x02 and y01 <= y11 and y11 <= y02 and y12 <= y02):
        return True
    return False

def zero(x):
    if x < 0 :
        return 0
    else:
        return x

if __name__=="__main__":
    # srcPath = 'C:\\person-property-2\\10\\'
    savePath  = 'D:\\dataset\\nuoya_ride_fankakou_patch\\'  # 存放modify的图片
    savePath1 = 'D:\\dataset\\nuoya_ride_fankakou_patch1\\' #存放modify的图片
    detect_file = open('D:\\dataset\\person-property\\fankakou_original_detect.txt','r') #detect
    pic_file = open('D:\\dataset\\person-property\\nuoya-ride-fankakou.list','r')
    pic_list = pic_file.readlines() #pic list

    detect_result = open('D:\\dataset\\test_nuoya_ride_fankakou\\detect-local.txt','r') #detect result
    detect_line = detect_result.readline()
    detect_list = []
    while detect_line:
        if detect_line.strip().endswith('.jpg'):
            patch_list = []
            patch_list.append(detect_line)
            b = int(detect_result.readline())
            # print box2
            for i in range(b):
                de_list = detect_result.readline().split(' ')
                patch_list.append(de_list)
        detect_list.append(patch_list)
        detect_line = detect_result.readline()
    print len(detect_list)


    line = detect_file.readline()
    out_file = open('D:\\dataset\\person-property\\nuoya_fankakou_cut_list.txt', 'a+')  # 图片的匹配情况
    # dirs = os.listdir(srcPath)  # 仅返回一级目录
    total_count=0

    while line:
        original = line.split(',')[0].strip()
        detect = line.split(',')[1].strip()
        information = original.split('_')  #picture information
        count = int(information[3]) #count
        imgPath = pic_list[count]
        print imgPath
        box1 = map(int, (information[6].split('-')[0],information[6].split('-')[1],information[6].split('-')[2],information[6].split('-')[3]))
        x1 , y1 , w1 , h1 = box1
        box1 = map(int, (x1, y1, x1+w1, y1+h1))

        a =imgPath.split('.jpg')[0]
        if os.path.exists(a + '.xml'):
            xmlPath = a + '.xml'
            try:
                xml_tree = open(xmlPath, 'r').read()  # 返回XML形式的字符串
                xml = et.XML(xml_tree)
            except:
                continue

             # patch_count=0
            for object in xml.iter('Object'):  # 遍历标注目标

                try:  # sn  type 是否存在
                    type = object.attrib['type']  # 类型
                except:
                    continue

                if type == 'non-motorized' :  # 骑行

                    # fullPosition = object.find('FullPosition')
                    if object.find('PersonProperty') is not None:
                        if object.find('PersonProperty').find('PersonCyclePos') is not None:
                            fullPosition1 = object.find('PersonProperty').find('PersonCyclePos')
                            x3, y3, w3, h3 = map(int, fullPosition1.text.split(','))  # 赋值

                            if h3 >= 500 :
                                continue

                            box3 = map(int, (x3, y3, x3 + w3, y3 + h3))  # 获取真实图片上的矩形框
                            if mat_inter(box1, box3):
                                if contains(box1,box3) :
                                    position3 = map(int, (x3-x1, y3-y1, w3, h3)) #相对于整体框的坐标
                                    position3 = list(map(zero, position3))
                                    box3_str = "-".join(['0' * (4 - len(str(x))) + str(x) for x in position3])
                                    information[6] = box3_str

                    for person in object.iter('Person'):
                        fullPosition1 = person.find('Position')
                        x3, y3, w3, h3 = map(int, fullPosition1.text.split(','))  # 赋值

                        box3 = map(int, (x3, y3, x3 + w3, y3 + h3))  # 获取真实图片上的矩形框
                        if mat_inter(box1, box3):
                            if contains(box1, box3):
                                position3 = map(int, (x3 - x1, y3 - y1, w3, h3))  # 相对于整体框的坐标
                                position3 = list(map(zero, position3))
                                box3_str = "-".join(['0' * (4 - len(str(x))) + str(x) for x in position3])
                                information[6] = box3_str

                    for bike in object.iter('NonMotor'):
                        fullPosition2 = bike.find('CycleBox')
                        x3, y3, w3, h3 = map(int, fullPosition2.text.split(','))  # 赋值
                        box3 = map(int, (x3, y3, x3 + w3, y3 + h3))  # 获取真实图片上的矩形框
                        if mat_inter(box1, box3):
                            if suit(box1, box3):
                                position3 = map(int, (x3 - x1, y3 - y1, w3, h3))  # 相对于整体框的坐标
                                position3 = list(map(zero, position3))
                                box3_str = "-".join(['0' * (4 - len(str(x))) + str(x) for x in position3])
                                information[6] = box3_str


            # exit(0)
        shutil.copy(savePath+original , savePath1+"_".join(information))  # 此处须给出绝对路径


        #处理detect图片
        detect_info = detect.split('_')
        box2 = map(int, (detect_info[6].split('-')[0], detect_info[6].split('-')[1], detect_info[6].split('-')[2],
                        detect_info[6].split('-')[3]))
        x2, y2, w2, h2 = box2
        box2 = map(int, (x2, y2, x2 + w2, y2 + h2))
         # if detect_line.strip() == imgPath.strip():
         # detect_img = []
        de_list = detect_list[count]
        print de_list[0]
        for i in range(1,len(de_list)):
            if de_list[i][5] == '4\n':
                box5 = map(int, (de_list[i][0], de_list[i][1], de_list[i][2], de_list[i][3]))
                if mat_inter(box2, box5):
                    if suit(box2,box5) :
                        position5 = map(int, (box5[0] - x2, box5[1] - y2, box5[2]-x2, box5[3]-y2))
                        position5 = list(map(zero, position5))
                        box5_str = "-".join(['0' * (4 - len(str(x))) + str(x) for x in position5])
                        detect_info[6] = box5_str
                    else:
                        continue
                else:
                    continue
            if de_list[i][5] == '5\n':
                box6 = map(int, (de_list[i][0], de_list[i][1], de_list[i][2], de_list[i][3]))
                if mat_inter(box2, box6):
                    if suit(box2,box6) :
                        position6 = map(int, (box6[0] - x2, box6[1]- y2, box6[2]-x2, box6[3]-y2))
                        position6 = list(map(zero, position6))
                        box6_str = "-".join(['0' * (4 - len(str(x))) + str(x) for x in position6])
                         # print box6_str
                        detect_info[7] = box6_str
                    else:
                        continue
                else:
                    continue
        shutil.copy(savePath + original, savePath1 + "_".join(detect_info))  # 此处须给出绝对路径

        total_count +=1
        line = detect_file.readline()
        out_file.write(savePath1+"_".join(information) + ' -- '+savePath1 + "_".join(detect_info) +'\n')

print(total_count)
out_file.close()







