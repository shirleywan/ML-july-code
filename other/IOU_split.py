# -*- coding: utf-8 -*-
import os
import shutil
from collections import Counter

#根据IOU划分query patch和detect patch，复制到不同一个文件夹下

id_location = 6
if __name__=="__main__":
    IOU_file = open('G:\\srcframe\\test_patch_detect.txt','r')
    IOU_line = IOU_file.readline() #pic list
    gtPath = 'G:\\patch\\patch_query\\'  # gt pic
    savePath = 'G:\\patch\patch_part\\' #savepath

    detect_list = os.listdir(gtPath)
    IOU_dict = {}
    count = {}
    while IOU_line:
        if IOU_line.strip().startswith('original patch'):
            if len(IOU_line.split(':')) < 2 :
                continue
            gtPic = IOU_line.strip().split('/')[-1] #take the gtname
            gtID = '_'.join(gtPic.split('_')[:id_location])
            IOU_line = IOU_file.readline()
            IOU_line = IOU_file.readline()
            IOU_num = IOU_line.strip().split(" ")[1]
            IOU_dict[gtID] = float(IOU_num)
        if IOU_line.strip().startswith('detect patch'):
            if len(IOU_line.split(':')) < 2 :
                continue
            gtPic = IOU_line.strip().split('/')[-1] #take the gtname
            gtID = '_'.join(gtPic.split('_')[:id_location])
            IOU_line = IOU_file.readline()
            IOU_num = IOU_line.strip().split(" ")[1]
            IOU_dict[gtID] = float(IOU_num)
            IOU_line = IOU_file.readline()
        IOU_line = IOU_file.readline()
    print len(IOU_dict)

    #name_list = []
    if not os.path.exists(os.path.join(savePath, "5" )):
        os.mkdir(os.path.join(savePath, "5" ))
    if not os.path.exists(os.path.join(savePath, "6" )):
        os.mkdir(os.path.join(savePath, "6" ))
    if not os.path.exists(os.path.join(savePath, "7" )):
        os.mkdir(os.path.join(savePath, "7" ))
    if not os.path.exists(os.path.join(savePath, "8" )):
        os.mkdir(os.path.join(savePath, "8" ))
    if not os.path.exists(os.path.join(savePath, "9" )):
        os.mkdir(os.path.join(savePath, "9" ))

    count = 0
    for i in range(len(detect_list)):
        picID = '_'.join(detect_list[i].split('_')[:id_location])
        picNum = IOU_dict[picID]
        IOU_num = int (float(picNum) / 0.1)
        if IOU_num < 6:
            imgPath = os.path.join(savePath, "5" ,detect_list[i])
            shutil.copy(gtPath + detect_list[i], imgPath)  # 此处须给出绝对路径
            count +=1

        if IOU_num >= 6 and IOU_num < 7:
            imgPath = os.path.join(savePath, "6" ,detect_list[i])
            shutil.copy(gtPath + detect_list[i], imgPath)  # 此处须给出绝对路径
            count +=1

        if IOU_num >= 7 and IOU_num < 8:
            imgPath = os.path.join(savePath, "7" ,detect_list[i])
            shutil.copy(gtPath + detect_list[i], imgPath)  # 此处须给出绝对路径
            count +=1

        if IOU_num >= 8 and IOU_num < 9:
            imgPath = os.path.join(savePath, "8" ,detect_list[i])
            shutil.copy(gtPath + detect_list[i], imgPath)  # 此处须给出绝对路径
            count +=1
        if IOU_num >= 9:
            imgPath = os.path.join(savePath, "9" ,detect_list[i])
            shutil.copy(gtPath + detect_list[i], imgPath)  # 此处须给出绝对路径
            count +=1
    print count



