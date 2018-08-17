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
# reload(sys)
# sys.setdefaultencoding('utf8')
#骑行图片的截取，也分为卡口、泛卡口；

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
    savePath = 'G:\\meiti-kakou\\meiti-kakou-patch2\\' #存放截好的图片
    detect_file = open('F:\\dataset\\jfr_box\\test_meiti_ride_kakou\\detect-local.txt','r') #detect
    line = detect_file.readline()
    out_file = open('G:\\meiti-kakou\\detect-meiti-kakou-patch2.txt', 'a+')  # 图片的匹配情况
    # dirs = os.listdir(srcPath)  # 仅返回一级目录
    count = 0
    patch_count = 0
    whole_id = 0
    while line:
        line = line.strip()
        if line.endswith('.jpg'):
            detect_img=[]
            a=line.split('.jpg')[0]
            # print a+'.jpg'
            b=detect_file.readline()
            b=int(b)
            for i in range(b):
                line = detect_file.readline()
                list = line.split(' ')
                box2 = map(int, (list[0], list[1], list[2], list[3],list[5]))
                detect_img.append(box2)
            # print detect_img


            if os.path.exists(a + '.xml'):
                xmlPath = a + '.xml'
                try:
                    xml_tree = open(xmlPath, 'r').read()  # 返回XML形式的字符串
                    xml = et.XML(xml_tree)
                except:
                    continue

                patch_count=0
                for object in xml.iter('object'):  # 遍历标注目标
                    area_list = []  # 每张真实图片生成一个list
                    try:  # sn  type 是否存在
                        type = object.find('name').text  # 类型
                    except:
                        continue


                    if type == 'rideall' or type == 'Rideall':  # 骑行
                        # 外接框  从frame中截取patch
                        # fullPosition = object.find('Position')
                        # fullPosition = object.find('FullPosition')

                        fullPosition = object.find('bndbox')

                        # fullPosition = object.find('FullPosition')

                        if fullPosition is None:
                            continue
                        # x, y, w, h = map(float, fullPosition.text.split(','))  # 赋值
                        x = int(fullPosition.find('xmin').text)
                        y = int(fullPosition.find('ymin').text)
                        w = int(fullPosition.find('xmax').text) - x
                        h = int(fullPosition.find('ymax').text) - y

                        if h < 500:
                            continue

                        box1=map(int,(x,y,x+w,y+h))  #获取真实图片上的矩形框
                        position1 = map(int, (x, y, w, h))  # 相对于整体框的坐标
                        imgPath = a + '.jpg'  # 第一个文件
                        print imgPath
                        # print "box1: ",box1
                        img = im.open(imgPath)
                        box3_list = []
                        box4_list = []


                        for object in xml.iter('object'):  # 遍历标注目标

                            try:  # sn  type 是否存在
                                type = object.find('name').text  # 类型
                            except:
                                continue

                            if type == 'cyclist' or type == 'Cyclist':  # 骑行人
                                fullPosition3 = object.find('bndbox')

                                # fullPosition = object.find('FullPosition')
                                if fullPosition3 is None:
                                    continue
                                # x, y, w, h = map(float, fullPosition.text.split(','))  # 赋值
                                x3 = int(fullPosition3.find('xmin').text)
                                y3 = int(fullPosition3.find('ymin').text)
                                w3 = int(fullPosition3.find('xmax').text) - x3
                                h3 = int(fullPosition3.find('ymax').text) - y3

                                box3 = map(int, (x3, y3, x3 + w3, y3 + h3))  # 获取真实图片上的矩形框
                                if mat_inter(box1, box3):
                                    area = solve_coincide(box1, box3)
                                    box3_list.append((area, box3))  # 形成元组


                            if type == 'motorbike' or type == 'bike' or type == 'Motorbike' or type == 'Bike':  # 骑行工具
                                fullPosition4 = object.find('bndbox')

                                # fullPosition = object.find('FullPosition')

                                if fullPosition4 is None:
                                    continue
                                # x, y, w, h = map(float, fullPosition.text.split(','))  # 赋值
                                x4 = int(fullPosition4.find('xmin').text)
                                y4 = int(fullPosition4.find('ymin').text)
                                w4 = int(fullPosition4.find('xmax').text) - x4
                                h4 = int(fullPosition4.find('ymax').text) - y4

                                box4 = map(int, (x4, y4, x4 + w4, y4 + h4))  # 获取真实图片上的矩形框
                                if mat_inter(box1, box4):
                                    area = solve_coincide(box1, box4)
                                    box4_list.append((area, box4))  # 形成元组
                                    # information[7] = box4_str
                        box3_list = sorted(box3_list, key=lambda box3_list: box3_list[0], reverse=True)
                        if len(box3_list) != 0:
                            box3 = box3_list[0][1]
                            # print "box3: ", box3
                            x3 = max(box3[0], box1[0])
                            y3 = max(box3[1], box1[1])
                            # print x3 , y3
                            position3 = map(int, (box3[0] - box1[0], y3 - box1[1], box3[2] - x3, box3[3] - y3))  # 相对于整体框的坐标
                            box3_str = "-".join(['0' * (4 - len(str(x))) + str(x) for x in position3])
                        else:
                            position1 = map(int, (0, 0, w, h))  # 相对于整体框的坐标
                            box3_str = "-".join(['0' * (4 - len(str(x))) + str(x) for x in position1])
                        # print "box3_str: " , box3_str

                        box4_list = sorted(box4_list, key=lambda box4_list: box4_list[0], reverse=True)
                        if len(box4_list) != 0:
                            box4 = box4_list[0][1]
                            x4 = max(box4[0], box1[0])
                            y4 = max(box4[1], box1[1])
                            position4 = map(int, (x4 - box1[0], y4 - box1[1], box4[2]-x4, box4[3]-y4))  # 相对于整体框的坐标
                            box4_str = "-".join(['0' * (4 - len(str(x))) + str(x) for x in position4])
                        else:
                            box4_str = "0000-0000-0000-0000"
                        # print "box4_str: " + box4_str

                        tImg1 = img.crop(box1)  # 设置要裁剪的区域
                        nowTime = datetime.datetime.now().strftime('%Y%m%d%H%M')
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
                            nowTime) + '_' + str_whole_id + '_' + str_patch_count + '_' + str_count + '_' + box3_str + '_' + box4_str + '_011110' + '.png'
                        tImg1.save(savePath + imgName)  # 存储在savepath路径下
                        out_file.write("original picture: " + imgPath + '\n')
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

                        if len(area_list) !=0 :

                            box2 = area_list[0][1]

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
                                position2 = map(int, (0, 0, box2[2] - box2[0] , box2[3] - box2[1]))
                                box5_str = "-".join(['0' * (4 - len(str(x))) + str(x) for x in position2])
                            else:
                                box5 = box5_list[0][1]
                                box5[0] = max(box5[0],box2[0])
                                box5[1] = max(box5[1], box2[1])
                                position5 = map(int,(box5[0] - box2[0],box5[1]-box2[1],box5[2]-box5[0],box5[3]-box5[1]))
                                box5_str = "-".join(['0' * (4 - len(str(x))) + str(x) for x in position5])
                            # print "box5_str: " + box5_str

                            box6_list = sorted(box6_list, key=lambda box6_list: box6_list[0], reverse=True)
                            if len(box6_list) == 0:
                                box6_str = "0000-0000-0000-0000"
                            else:
                                box6 = box6_list[0][1]
                                box6[0] = max(box6[0], box2[0])
                                box6[1] = max(box6[1], box2[1])
                                position6 = map(int, (box6[0]-box2[0], box6[1]-box2[1], box6[2] - box6[0], box6[3] - box6[1]))
                                box6_str = "-".join(['0' * (4 - len(str(x))) + str(x) for x in position6])

                            tImg2 = img.crop(box2)  # 设置要裁剪的区域
                            de_imgname ='HY0_0000_'+str(nowTime)+'_' + str_whole_id + '_' + str_patch_count + '_' + str_count + '_'+box5_str+'_'+box6_str+'_011111'+'.png'
                            tImg2.save(savePath + de_imgname)  # 存储在savepath路径下
                            # print "imgName: ",imgName
                            # print "de_imgname: ", de_imgname
                            out_file.write("detect patch: " + de_imgname + '\n')
                        whole_id += 1
                        patch_count += 1

                    else:
                        continue

            count += 1
            patch_count = 0
        line = detect_file.readline()
        # exit(0)
print(count)
out_file.close()







