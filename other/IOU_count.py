# -*- coding: utf-8 -*-
import os
from collections import Counter

#从已有的GTpatch-detectPatch-IOU的list中，统计某个文件夹下图片各IOU比例的个数

id_location = 6
if __name__=="__main__":
    IOU_file = open('G:\\srcframe\\test_patch_detect.txt','r')
    IOU_line = IOU_file.readline() #pic list
    gtPath = 'G:\\patch\\patch_query\\'  # gt pic

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

    total_count = []
    for i in range(len(detect_list)):
        picID = '_'.join(detect_list[i].split('_')[:id_location])
        picNum = IOU_dict[picID]
        total_count.append(int (float(picNum) / 0.1))

    dic = Counter(total_count)
    print [(k, dic[k]) for k in sorted(dic.keys())]
