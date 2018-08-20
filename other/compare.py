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
#IOU实验，用来从原始帧图片中截取detect-patch，对应的GT-patch与原始帧图片命名相同；

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


if __name__=="__main__":
    savePath = 'G:/detect_patch/detect_patch/' #存放截好的图片
    detect_file = open('G:\\srcframe\\test_patch240000\\detect.txt','r') #detect
    # detect_file = open('G:\\srcframe\\test_patch240000\\detect-test.txt', 'r')  # detect
    line = detect_file.readline()
    out_file = open('G:\\srcframe\\test_patch_detect.txt', 'a+')  # 图片的匹配情况
    # dirs = os.listdir(srcPath)  # 仅返回一级目录
    count = 0
    while line:
        line = line.strip()
        if line.endswith('.jpg'):
            imgPath = line
            name = line

            split_list = line.split('/')
            size_list = split_list[3].split('_')
            box1 = map(int,(size_list[6:10]))

            overlap_list = []
            b=detect_file.readline() #detect结果数量
            b=int(b)
            for i in range(b):
                line = detect_file.readline()
                detect_list = line.split(' ')
                if int(detect_list[5]) == 1:
                    box2 = map(int, (detect_list[0:4]))
                    if mat_inter(box1, box2):
                        area = solve_coincide(box1, box2)
                        overlap_list.append((area, box2))  # 形成元组

            overlap_list = sorted(overlap_list, key=lambda overlap_list: overlap_list[0], reverse=True)
            if len(overlap_list) > 0:
                box2 = overlap_list[0][1]
                box2_str = "_".join(['0' * (4 - len(str(x))) + str(x) for x in box2])
                info_str = size_list[14][0:5] +"1"+size_list[14][6:10]
                de_imgname = "_".join([ str(x) for x in size_list[0:6]])+"_" +box2_str +"_"+"_".join(
                            [ str(x) for x in size_list[10:14]])+"_"+ info_str

                img = im.open(imgPath)
                print imgPath
                tImg2 = img.crop(box2)  # 设置要裁剪的区域
                tImg2.save(savePath + de_imgname)  # 存储在savepath路径下
                out_file.write("original patch: " + name + '\n')
                out_file.write("detect patch: " + savePath+de_imgname + '\n')
                out_file.write("overlap: "+overlap_list[0][0] +'\n')
                print savePath+de_imgname

        count += 1
        line = detect_file.readline()

print(count)
out_file.close()







