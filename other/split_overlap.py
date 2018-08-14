# -*- coding: utf-8 -*-
import os
import shutil
import math


def getID(filename):
    subNames = filename.split('_')
    return '_'.join(subNames[:4])

if __name__=="__main__":
    savePath = 'G:/overlap/' #存放截好的图片
    read_file = open('G:\\srcframe\\test_patch_detect.txt','r') #detect
    # detect_file = open('G:\\srcframe\\test_patch240000\\detect-test.txt', 'r')  # detect
    line = read_file.readline()
    imgIDs = []
    count = 0
    while line:
        if line.strip().startswith("original patch"):
            patch_path = line.strip().split(" ")[2]
            imgName = patch_path.split('/')[3] #GT_patch的名称

            line = read_file.readline()
            detect_path = line.strip().split(" ")[2]
            detectName = detect_path.split('/')[3] #detect_patch的名称

            line = read_file.readline() #overlap num
            num = line.strip().split(" ")[1]
            num = int (float(num) / 0.1)
            if not os.path.exists(savePath +'/'+str(num)+'/patch'):
                os.makedirs(savePath +'/'+str(num)+'/patch')
            if not os.path.exists(savePath +'/'+str(num)+'/detect'):
                os.makedirs(savePath +'/'+str(num)+'/detect')

            shutil.copy(patch_path, savePath + '/'+str(num)+"/patch/"+imgName)
            shutil.copy(patch_path, savePath + '/'+str(num) + "/detect/" + detectName)
            print num

            exit(0)

        line = read_file.readline()
