# -*- coding: utf-8 -*-
import os
from PIL import Image as im
import xml.etree.cElementTree as et
import datetime
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from textwrap import wrap
import xml.dom.minidom as minidom
import sys
import re
# reload(sys)
# sys.setdefaultencoding('utf8')
#诺亚骑行泛卡口patch截取和重命名；

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

def contains(box1,box2):
    x01, y01, x02, y02 = box1
    x11, y11, x12, y12 = box2
    if(x01 <= x11 and x11 <= x02 and x12 <= x02 and y01 <= y11 and y11 <= y02 and y12 <= y02):
        return True
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


def zero(x):
    if x < 0 :
        return 0
    else:
        return x

def suit(box1,box2):
    if solve_coincide(box1,box2) > 0.8:
        return True
    return False


if __name__=="__main__":
    # srcPath = 'C:\\person-property-2\\10\\'
    savePath = 'G:\\nuoya-fankakou\\nuoya-fankakou-patch\\' #存放截好的图片
    # detect_file = open('D:\\dataset\\test_nuoya_ride_fankakou\\detect-local.txt','r') #detect
    detect_file = open('D:\\dataset\\test_nuoya_ride_fankakou\\detect-local.txt','r')
    line = detect_file.readline()
    out_file = open('G:\\nuoya-fankakou\\detect-nuoya-fankakou.txt', 'a+')  # 图片的匹配情况
    # dirs = os.listdir(srcPath)  # 仅返回一级目录
    count = 0
    patch_count = 0
    whole_id = 0

    while line :
        # if line.strip() != 'D:/dataset/person-property/1/0734a007-1/A0814107-1_00000507.jpg':
        #     line = detect_file.readline()
        #     continue
        line = line.strip()
        if line.endswith('.jpg'):
            detect_img=[]
            a=line.split('.jpg')[0]
            b=detect_file.readline()
            b=int(b)
            for i in range(b):
                line = detect_file.readline()
                list_de = []
                list_de = line.split(' ')
                box2 = map(int, (list_de[0], list_de[1], list_de[2], list_de[3],list_de[5]))
                # if list_de[0] >= list_de[2] or list_de[1] >= list_de[3] :
                #     continue
                detect_img.append(box2)
            # print detect_img
            # print detect_img


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

                    if type == 'non-motorized':  # 骑行

                        fullPosition = None
                        if object.find("FullPosition") is not None:
                            fullPosition = object.find('FullPosition')
                            if fullPosition is None:
                                continue
                            x1, y1, w1, h1 = map(float, fullPosition.text.split(','))
                            box1 = map(int , (x1, y1, x1+w1 , y1+h1))
                            if h1 >= 500:
                                continue
                            if w1 <= 0 or h1 <=0 :
                                continue
                            position1 = map(int, (0, 0, w1, h1))
                            box3_str = "-".join(['0' * (4 - len(str(x))) + str(x) for x in position1])
                            box4_str = "0000-0000-0000-0000"
                            if object.find('PersonProperty') is not None:
                                if object.find('PersonProperty').find('PersonCyclePos') is not None:
                                    fullPosition1 = object.find('PersonProperty').find('PersonCyclePos')
                                    x3, y3, w3, h3 = map(int, fullPosition1.text.split(','))  # 赋值
                                    box3 = map(int, (x3, y3, x3 + w3, y3 + h3))  # 获取真实图片上的矩形框
                                    if mat_inter(box1, box3):
                                        if contains(box1, box3):
                                            position3 = map(int, (x3 - x1, y3 - y1, w3, h3))  # 相对于整体框的坐标
                                            position3 = list(map(zero, position3))
                                            box3_str = "-".join(['0' * (4 - len(str(x))) + str(x) for x in position3])

                        else:
                            if object.find("PersonCyclePos") is not None:
                                fullPosition = object.find('PersonCyclePos')
                                if fullPosition or fullPosition.text is None:
                                    continue

                                x1, y1, w1, h1 = map(int, str(fullPosition.text).split(','))

                                box1 = map(int, (x1, y1, x1 + w1, y1 + h1))
                                if h1 >= 500:
                                    continue
                                box3_str = "-".join(['0' * (4 - len(str(x))) + str(x) for x in position1])
                                box4_str = "0000-0000-0000-0000"
                                for person in object.iter('Person'):
                                    fullPosition1 = person.find('Position')
                                    if fullPosition1 is None:
                                        continue
                                    x3, y3, w3, h3 = map(int, fullPosition1.text.split(','))  # 赋值

                                    box3 = map(int, (x3, y3, x3 + w3, y3 + h3))  # 获取真实图片上的矩形框
                                    x3 = max(x3, x1)
                                    y3 = max(y3, y1)
                                    position3 = map(int, (x3 - x1, y3 - y1, w3, h3))  # 相对于整体框的坐标
                                    box3_str = "-".join(['0' * (4 - len(str(x))) + str(x) for x in position3])
                                for bike in object.iter('NonMotor'):
                                    fullPosition2 = bike.find('CycleBox')
                                    if fullPosition2 is None:
                                        continue
                                    x4, y4, w4, h4 = map(int, fullPosition2.text.split(','))  # 赋值
                                    box4 = map(int, (x4, y4, x4 + w4, y4 + h4))  # 获取真实图片上的矩形框
                                    x4= max(x4,x1)
                                    y4 = max(y4,y1)
                                    position4 = map(int, (x4 - x1, y4 - y1, w4, h4))  # 相对于整体框的坐标
                                    box4_str = "-".join(['0' * (4 - len(str(x))) + str(x) for x in position4])
                            else:
                                continue

                        if fullPosition is None:
                            continue

                        patch_count += 1
                        nowTime = datetime.datetime.now().strftime('%Y%m%d%H%M')
                        imgPath = a + '.jpg'  # 第一个文件
                        print imgPath
                        img = im.open(imgPath)
                        # position1=map(int,(x, y, w, h))
                        # position2=map(int,(box2[0],box2[1],box2[2]-box2[0],box2[3]-box2[1]))
                        # box1_str="-".join(['0'*(4-len(str(x)))+str(x) for x in position1])
                        # box2_str="-".join(['0'*(4-len(str(x)))+str(x) for x in position2])
                        str_count = '0' * (8 - len(str(count))) + str(count)
                        str_patch_count = '0' * (3 - len(str(patch_count))) + str(patch_count)
                        str_whole_id = '0' * (8 - len(str(whole_id))) + str(whole_id)
                        # print(box1_str)
                        # print(box2_str)
                        imgName = 'HY0_0000_' + str(
                            nowTime) + '_' + str_whole_id + '_' + str_patch_count + '_' + str_count + '_' + box3_str + '_' + box4_str + '_111120' + '.png'
                        tImg1 = img.crop(box1)  # 设置要裁剪的区域
                        tImg1.save(savePath + imgName)  # 存储在savepath路径下
                        out_file.write("original picture: " +imgPath +'\n')
                        out_file.write("original patch: " + imgName + '\n')


                        area_list = []
                        for i in range(len(detect_img)):
                            new_box = detect_img[i]
                            if int(new_box[4]) == 3:
                                box2 = map(int, (new_box[0], new_box[1], new_box[2], new_box[3]))
                                if mat_inter(box1,box2) :
                                    area=solve_coincide(box1,box2)
                                    area_list.append((area,box2)) #形成元组

                        area_list = sorted(area_list, key=lambda area_list: area_list[0], reverse=True)
                        # patch_count +=1
                        # print(area_list)

                        if len(area_list) > 0:
                            box2 = area_list[0][1]
                            # print "box2: ",box2


                            box5_list = []
                            box6_list = []
                            for i in range(len(detect_img)):
                                new_box = detect_img[i]
                                if int(new_box[4]) == 4 :
                                    box5 = map(int, (new_box[0], new_box[1], new_box[2], new_box[3]))
                                    if mat_inter(box2,box5) :
                                        area=solve_coincide(box2,box5)
                                        box5_list.append((area,box5)) #形成元组

                                if int(new_box[4]) == 5:
                                    box6 = map(int, (new_box[0], new_box[1], new_box[2], new_box[3]))
                                    if mat_inter(box2, box6):
                                        area = solve_coincide(box2, box6)
                                        box6_list.append((area, box6))  # 形成元组

                            box5_list = sorted(box5_list, key=lambda box5_list: box5_list[0], reverse=True)
                            if len(box5_list)==0 :
                                position2 = map(int, (0, 0, box2[2] - box2[0], box2[3] - box2[1]))
                                box5_str = "-".join(['0' * (4 - len(str(x))) + str(x) for x in position2])
                            else:
                                box5 = box5_list[0][1]
                                box5[0] = max(box5[0],box2[0])
                                box5[1] = max(box5[1], box2[1])
                                # print box5[0] , box5[1]
                                position5 = map(int,(box5[0] - box2[0],box5[1]-box2[1],box5[2]-box5[0],box5[3]-box5[1]))
                                box5_str = "-".join(['0' * (4 - len(str(x))) + str(x) for x in position5])
                                # print box5_str

                            box6_list = sorted(box6_list, key=lambda box6_list: box6_list[0], reverse=True)
                            if len(box6_list) == 0:
                                box6_str = "0000-0000-0000-0000"
                            else:
                                box6 = box6_list[0][1]
                                box6[0] = max(box6[0], box2[0])
                                box6[1] = max(box6[1], box2[1])
                                position6 = map(int, (box6[0]-box2[0], box6[1]-box2[1], box6[2] - box6[0], box6[3] - box6[1]))
                                box6_str = "-".join(['0' * (4 - len(str(x))) + str(x) for x in position6])
                            # print box6_str

                            de_imgname = 'HY0_0000_' + str(
                                nowTime) + '_' + str_whole_id + '_' + str_patch_count + '_' + str_count + '_' + box5_str + '_' + box6_str + '_111121' + '.png'
                            tImg2 = img.crop(box2)  # 设置要裁剪的区域
                            tImg2.save(savePath + de_imgname)  # 存储在savepath路径下
                            out_file.write("detect patch: " + de_imgname + '\n')

                        whole_id += 1
                        patch_count += 1

            count += 1
            patch_count = 0
            # exit(0)
        line = detect_file.readline()
        # exit(0)
print(count)
out_file.close()







