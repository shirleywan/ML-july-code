# -*- coding: utf-8 -*-
import os
import numpy as np
import shutil
# query，gallery划分
srcpath='G:/detect_patch/gallery/'
savepath="G:/detect_patch/query/"
imgIDs=[]
def getCam(filename):
        subNames = filename.split('_')
        return '_'.join(subNames[:5])

def FindOneIDperCam(srcpath):
    count=0 
    imglist = os.listdir(srcpath)
    for imgName in imglist:
        ext=os.path.splitext(imgName)[1] #将文件名和扩展名分开
        if ext != ".jpg": 
            continue
        imgpath = os.path.join(srcpath,imgName)
        imgID = getCam(imgName)
        savepathall=os.path.join(savepath,imgName)
        if imgID not in imgIDs:
            imgIDs.append(imgID)
            os.rename(imgpath,savepathall)
            count+=1
    print count            
if __name__ == '__main__': 
         FindOneIDperCam(srcpath)
    


