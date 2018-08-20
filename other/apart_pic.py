import os
import numpy as np
# import cv2
import multiprocessing as mtp
import math
import logging
import time
import shutil


dir1= '/home/miaojiaxu/data/large/back'
dir2= '/home/miaojiaxu/data/large/front'
dir3= '/home/miaojiaxu/data/large/left'
dir4= '/home/miaojiaxu/data/large/right'
new4= '/home/miaojiaxu/data/large/new_right'
ori1={}
ori2={}
ori3={}
ori4={}
i=0
pid=0
pid1=0
pid2=0
pid3=0
for line in open(dir1+'.list').readlines():
    ori1[pid]=line[0:28]
    pid=pid+1
for line in open(dir2+'.list').readlines():
    ori2[pid1]=line[0:28]
    pid1=pid1+1
for line in open(dir3+'.list').readlines():
    ori3[pid2]=line[0:28]
    pid2=pid2+1
for line in open(dir4+'.list').readlines():
    ori4[pid3]=line[0:28]
    pid3=pid3+1
    # ori4[hashvalue]=os.path.join(dir3,filename)
for filename in os.listdir(dir4):
	# ori4 = filename [0:28]
    if ori4 in ori1 and ori4 in ori2 and ori4 in ori3:
        # print ori4
        shutil.copy(os.path.join(dir4,filename),os.path.join(new4,filename))
        i=i+1
