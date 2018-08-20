# -*- coding: utf-8 -*-
import os
from PIL import Image as im
import xml.etree.cElementTree as et
import datetime
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import re
from textwrap import wrap
import xml.dom.minidom as minidom
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
#诺亚行人卡口patch

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
    # srcPath = 'C:\\person-property-2\\10\\'
    savePath = 'D:\\dataset\\nuoya_ride_fankakou_patch\\' #存放截好的图片
    detect_file = open('D:\\dataset\\test_nuoya_ride_fankakou\\detect-local.txt','r') #detect
    line = detect_file.readline()
    out_file = open('D:\\dataset\\person-property\\detect_ride_fankakou.txt', 'a+')  # 图片的匹配情况
    # dirs = os.listdir(srcPath)  # 仅返回一级目录
    count=0
    while line:
        line = line.strip()
        if line.endswith('.jpg'):
            detect_img=[]
            a=line.split('.jpg')[0]
            b=detect_file.readline()
            b=int(b)
            for i in range(b):
                line = detect_file.readline()
                list = line.split(' ')
                if (list[0] >= list[2]) or (list[1] >= list[3]) :
                    continue
                box2 = map(int, (list[0], list[1], list[2], list[3]))
                detect_img.append(box2)


            if os.path.exists(a + '.xml'):
                xmlPath = a + '.xml'
                try:
                    xml_tree = open(xmlPath, 'r').read()  # 返回XML形式的字符串
                    xml = et.XML(xml_tree)
                except:
                    continue

                patch_count=0
                for object in xml.iter('Object'):  # 遍历标注目标
                    area_list = []  # 每张真实图片生成一个list
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


                        list = re.split(",", fullPosition)
                        x1 = int(list[0])
                        y1 = int(list[1])
                        w1 = int(list[2])
                        h1 = int(list[3])

                        if(w1< 0 or h1 < 0):
                            continue

                        if (h1 < 500) : #泛卡口
                            box1=map(int,(x1,y1,x1+w1,y1+h1))  #获取真实图片上的矩形框

                            for i in range(len(detect_img)):
                                box2 = detect_img[i]
                                if mat_inter(box1,box2) :
                                    area=solve_coincide(box1,box2)
                                    area_list.append((area,box2)) #形成元组

                            area_list = sorted(area_list, key=lambda area_list: area_list[0], reverse=True)
                            patch_count +=1
                            # print(area_list)

                            if len(area_list) > 0 :
                                box2 = area_list[0][1]
                                imgPath = a + '.jpg'  # 第一个文件
                                img = im.open(imgPath)
                                print(imgPath)

                                tImg1 = img.crop(box1)  # 设置要裁剪的区域
                                tImg2 = img.crop(box2)  # 设置要裁剪的区域
                                nowTime = datetime.datetime.now().strftime('%Y%m%d%H%M')
                                position1=map(int,(x1, y1, w1, h1))
                                position2=map(int,(box2[0],box2[1],box2[2]-box2[0],box2[3]-box2[1]))
                                box1_str="-".join(['0'*(4-len(str(x)))+str(x) for x in position1])
                                box2_str="-".join(['0'*(4-len(str(x)))+str(x) for x in position2])
                                str_count = '0' * (8 - len(str(count))) + str(count)
                                # print(box1_str)
                                # print(box2_str)
                                str_patch_count = '0'*(8-len(str(patch_count)))+str(patch_count)
                                # print(box1_str)
                                # print(box2_str)
                                imgName = 'HY0_0000_' + str(nowTime) + '_' + str_count + '_050_'+str_patch_count+'_' + box1_str + '_0000-0000-0000-0000_111120' + '.png'
                                tImg1.save(savePath + imgName)  # 存储在savepath路径下

                                de_imgname = 'HY0_0000_' + str(nowTime) + '_' + str_count + '_050_' +str_patch_count+'_'+ box2_str + '_0000-0000-0000-0000_111121' + '.png'
                                tImg2.save(savePath + de_imgname)  # 存储在savepath路径下
                                out_file.writelines('%s , %s ' % (imgName, de_imgname))
                                out_file.write('\n')

                    else:
                        continue
            count += 1
        line = detect_file.readline()
print(count)
out_file.close()







