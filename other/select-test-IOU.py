# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 21:46:28 2018

@author: x00444415
"""

import os
import cv2
import numpy as np
#import xml.etree.cElementTree as et
import xml.dom.minidom as rxml
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def checkPath(dir1):
        if not os.path.exists(dir1):
                os.makedirs(dir1)

src_xml = 'Y:/XiAn/data_origin/auto-label-test/1600_201806021600/xml'
src_img = 'Y:/XiAn/data_origin/auto-label-test/1600_201806021600/personID++-patch'
src_img2 = 'Y:/XiAn/data_origin/auto-label-test/1600_201806021600/personID++'

dst_09_a = 'D:/Re-ID/data_test/Label3/09_auto'
dst_09_h = 'D:/Re-ID/data_test/Label3/09_hm'
checkPath(dst_09_a)
checkPath(dst_09_h)

dst_08_a = 'D:/Re-ID/data_test/Label3/08_auto'
dst_08_h = 'D:/Re-ID/data_test/Label3/08_hm'
checkPath(dst_08_a)
checkPath(dst_08_h)

dst_07_a = 'D:/Re-ID/data_test/Label3/07_auto'
dst_07_h = 'D:/Re-ID/data_test/Label3/07_hm'
checkPath(dst_07_a)
checkPath(dst_07_h)

dst_06_a = 'D:/Re-ID/data_test/Label3/06_auto'
dst_06_h = 'D:/Re-ID/data_test/Label3/06_hm'
checkPath(dst_06_a)
checkPath(dst_06_h)

dst_05_a = 'D:/Re-ID/data_test/Label3/05_auto'
dst_05_h = 'D:/Re-ID/data_test/Label3/05_hm'
checkPath(dst_05_a)
checkPath(dst_05_h)

dst_04_a = 'D:/Re-ID/data_test/Label3/04_auto'
dst_04_h = 'D:/Re-ID/data_test/Label3/04_hm'
checkPath(dst_04_a)
checkPath(dst_04_h)

dst_03_a = 'D:/Re-ID/data_test/Label3/03_auto'
dst_03_h = 'D:/Re-ID/data_test/Label3/03_hm'
checkPath(dst_03_a)
checkPath(dst_03_h)

'''
with open(os.path.join(src_txt,'offset.txt'), 'r') as old_file:
    lines = old_file.readlines()
    print len(lines)
    
for i in range(len(lines)):
    if float(lines[0][23:31]) >= 0.9:
        
'''

def gettime(filename):
	subNames = filename.split('_')
	return '_'.join(subNames[:3])

def getframe(filename):
	subNames = filename.split('_')
	return subNames[5]

def getcam(filename):
	subNames = filename.split('_')
	return subNames[4]


files= os.listdir(src_img)
files.sort()
n = 0
for fileName in files:

    print (fileName,'is done')
    subname = os.path.join(src_img,fileName)

    if (os.path.isdir(subname)):
        os.chdir(subname)
        M1 = os.getcwd()
        M2 = os.path.join(src_xml,fileName)
        M3 = os.path.join(src_img2,fileName)
        print (M3)
        #print M1
        #print M2
        Imgs =[]
        Imgs = os.listdir(M1)
        Imgs.sort()
        num_img = len(Imgs)
        for ImgName in Imgs:
            idx = idx = ImgName.rfind('.')
            type_name = ImgName[idx+1:idx+3]
            if type_name != 'jp':
                continue
            time =[]
            cam =[]
            frame=[]
            #print ImgName
            time = gettime(ImgName)
            cam = getcam(ImgName)
            frame = getframe(ImgName)
            #print frame
            
            Xmlname = []
            Xmlname = time+'_'+cam+'_'+frame+'.xml'
            imgname = time+'_'+cam+'_'+frame+'.jpg'
            #print Xmlname
            #print M2
            #print os.path.join(M2,Xmlname)
            dom = rxml.parse(os.path.join(M2,Xmlname))
            root = []
            root = dom.documentElement
            
            auto = root.getElementsByTagName('rider_auto')
            hm = root.getElementsByTagName('rider')
            whole = root.getElementsByTagName('whole')
            #auto2 = root.getElementsByTagName('whole-auto')
            #auto3 = root.getElementsByTagName('cycle-auto')
            
            #left = int(whole[0].getAttribute('x'))
            #top = int(whole[0].getAttribute('y'))
            
            #print left
            #print top
            
            if len(auto) == 0:
                continue
            
            if len(auto)>0:
                 n = n + 1
                 x1 = int(auto[0].getAttribute('x'))
                 y1 = int(auto[0].getAttribute('y'))
                 w1 = int(auto[0].getAttribute('w'))
                 h1 = int(auto[0].getAttribute('h'))
                 rect1 = QRect(int(x1), int(y1), int(w1), int(h1))
                 
                 #print x1, y1, w1, h1
                 
                 x2 = int(hm[0].getAttribute('x'))
                 y2 = int(hm[0].getAttribute('y'))
                 w2 = int(hm[0].getAttribute('w'))
                 h2 = int(hm[0].getAttribute('h'))
                 
                 rect1 = QRect(int(x1), int(y1), int(w1), int(h1))
                 rect2 = QRect(int(x2), int(y2), int(w2), int(h2))
                 Inte = rect1 & rect2
                 Union = rect1 | rect2
                 
                 #print (Inte.width()*Inte.height())
                 #print (Union.width()*Union.height())
                 res = float(Inte.width()*Inte.height()) / float(Union.width()*Union.height())
                 #print res
                 
                 img = []
                 img = cv2.imread(os.path.join(M3,imgname))
                
                 
                 #x1 = x1 - left
                 #y1 = y1 - top
                 #y2 = y2 -top
                 #x2 = x2 -left
                 
                 #if x1<0:
                 #    x1=0
                 #if y1<0:
                 #    y1=0
                 #if y2<0:
                 #    y2=0
                 #if x2<0:
                 #    y2=0
                    
                 
                 #print y1
                 #print y1+h1
                 #print x1
                 #print x1+w1
                 #print img.shape[0]
                 #print img.shape[1]
                 #print 
                 if res>=0.9:
                     print ('res>0.9')
                     img_au = img[y1:y1+h1,x1:x1+w1]
                     img_hm = img[y2:y2+h2,x2:x2+w2]
                     cv2.imwrite(os.path.join(dst_09_a,ImgName),img_au)
                     cv2.imwrite(os.path.join(dst_09_h,ImgName),img_hm)
                
                 if (res<0.9) and (res>=0.8):
                    print ('0.8<=res<0.9')
                    img_au = img[y1:y1+h1,x1:x1+w1]
                    img_hm = img[y2:y2+h2,x2:x2+w2]
                    cv2.imwrite(os.path.join(dst_08_a,ImgName),img_au)
                    cv2.imwrite(os.path.join(dst_08_h,ImgName),img_hm)
                    
                 if (res<0.8) and (res>=0.7):
                    print ('0.7<=res<0.8')
                    img_au = img[y1:y1+h1,x1:x1+w1]
                    img_hm = img[y2:y2+h2,x2:x2+w2]
                    cv2.imwrite(os.path.join(dst_07_a,ImgName),img_au)
                    cv2.imwrite(os.path.join(dst_07_h,ImgName),img_hm)
                    
                 if (res<0.7) and (res>=0.6):
                    print ('0.6<=res<0.7')
                    img_au = img[y1:y1+h1,x1:x1+w1]
                    img_hm = img[y2:y2+h2,x2:x2+w2]
                    cv2.imwrite(os.path.join(dst_06_a,ImgName),img_au)
                    cv2.imwrite(os.path.join(dst_06_h,ImgName),img_hm)
                    
                 if (res<0.6) and (res>=0.5):
                    print ('0.5<=res<0.6')
                    img_au = img[y1:y1+h1,x1:x1+w1]
                    img_hm = img[y2:y2+h2,x2:x2+w2]
                    cv2.imwrite(os.path.join(dst_05_a,ImgName),img_au)
                    cv2.imwrite(os.path.join(dst_05_h,ImgName),img_hm)
                    
                 if (res<0.5) and (res>=0.4):
                    print ('0.4<=res<0.5')
                    img_au = img[y1:y1+h1,x1:x1+w1]
                    img_hm = img[y2:y2+h2,x2:x2+w2]
                    cv2.imwrite(os.path.join(dst_04_a,ImgName),img_au)
                    cv2.imwrite(os.path.join(dst_04_h,ImgName),img_hm)
                    
                 if (res<0.4) and (res>=0.3):
                    print ('0.4<=res<0.5')
                    img_au = img[y1:y1+h1,x1:x1+w1]
                    img_hm = img[y2:y2+h2,x2:x2+w2]
                    cv2.imwrite(os.path.join(dst_03_a,ImgName),img_au)
                    cv2.imwrite(os.path.join(dst_03_h,ImgName),img_hm)
                     
                 
                 
                
                
                
                
            
            '''
            if len(auto) >0:
                n = n +1
            if len(auto2) >0:
                n = n +1
            if len(auto3) >0:
                n = n +1
            
            
                
        print n
            '''


