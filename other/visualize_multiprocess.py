import os
import sys
import numpy as np
import cv2
import time
import math
import multiprocessing as mtp
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s : %(message)s')
#n_full = 39  #41

dataPath=os.path.join(sys.argv[1], 'gallery')
savePath=sys.argv[2]
queryPath=os.path.join(sys.argv[1], 'query')
resultPath=sys.argv[4]

cam_location = 4
id_location = 4
print "dataPath: ", dataPath
print "savePath: ", savePath
print "queryPath: ", queryPath
#resnet
img_suffix = '.jpg' #'.jpg'
if not os.path.exists(savePath):
    savePath=savePath.split('/')
    savePath=os.path.join('/'.join(savePath[:-1]),'archive',savePath[-1])
    print savePath

if not os.path.exists(resultPath):
    print 'No saved result found!'
    exit(0)

visualPath=os.path.join(resultPath,'visual')
if not os.path.exists(visualPath):
    os.mkdir(visualPath)

ids={}
for line in open(dataPath+'.list').readlines():
    id='_'.join(line.split('_')[:id_location])
    cam=line.split('_')[cam_location]
    if id not in ids.keys():
        ids[id]={}
    if cam not in ids[id].keys():
        ids[id][cam]=[]
    ids[id][cam].append(line[:-1])

#n=0
def visualize(proc,lock,count,rank_list,queryPath,dataPath,visualPath,img_suffix,ids):
    for rank in rank_list:
        combined=np.zeros((192,0,3))
        gtBar=np.zeros((192,96,3))
        org=cv2.imread(os.path.join(queryPath,rank.split('.')[0]+img_suffix))
        if org is None:
            print 'hello'
            print os.path.join(queryPath,rank.split('.')[0]+img_suffix)
            continue
        org=cv2.resize(org,(96,192))
        combined=np.append(combined,org,axis=1)

        rankFile=open(os.path.join(resultPath,'rankFiles',rank)).readlines()
        #id=rank[0:28]
        id='_'.join(rank.split('_')[:id_location])   #t2=time.time()
        if id not in ids.keys():
            print "the query is not in the gallery"
            continue
        for cam in ids[id].keys():
            #print os.path.join(dataPath, ids[id][cam][0][:-1])
            #print os.path.exists(os.path.join(dataPath, ids[id][cam][0][:-1]))
            img=cv2.imread(os.path.join(dataPath,ids[id][cam][0]))
            if img is None:
                print 'the image in None'
            img=cv2.resize(img,(96,192))
            label=cam
            cv2.putText(img,label,(65,12),0,0.5,(255,255,255),3)
            cv2.putText(img,label,(65,12),0,0.5,(0,0,0),2)
            gtBar=np.append(gtBar,img,axis=1)
        blackBar=np.zeros((192,96*(20-len(ids[id].keys())),3))
        gtBar=np.append(gtBar,blackBar,axis=1)
        #t3=time.time()
        for i in xrange(20) :
            #t31=time.time()
            #print rankFile[i]
            name=rankFile[i].split(' ')[0]+img_suffix
            #print name
            id2='_'.join(rankFile[i].split('_')[:id_location])
            img=cv2.imread(os.path.join(dataPath,name))
            #t32=time.time()
            img=cv2.resize(img,(96,192))
            #t33=time.time()
            label='x'
            color=(0,0,255)
            #print cam
            #print id
            #print ids[id][cam]
            #print name
            for cam in ids[id]:
                if name in ids[id][cam]:
                    label='o'
                    color=(60,255,60)
                    break
            #t34=time.time()
            #print label
            labelcam=rankFile[i].split('_')[cam_location]
            cv2.putText(img,label,(0,12),0,0.8,color,3)
            cv2.putText(img,labelcam,(75,10),0,0.3,(255,255,255),2)
            cv2.putText(img,labelcam,(75,10),0,0.3,(0,0,0),1)
            combined=np.hstack((combined,img))
            #t35=time.time()
            #t30=t35-t31
            #print '%.2f %.2f %.2f %.2f' % ((t32-t31)/t30,(t33-t32)/t30,(t34-t33)/t30,(t35-t34)/t30)
        #t4=time.time()
        combined=np.append(combined,gtBar,axis=0)
        point_pos=rank.find(".txt")
        #print os.path.join(visualPath,rank[0:point_pos]+'.jpg')
        cv2.imwrite(os.path.join(visualPath,rank[0:point_pos]+'.jpg'),combined)
        lock.acquire()
        count.value += 1
        lock.release()
        if count.value % 100 == 0:
            logging.info(str(count.value) + " query finished")
        #cv2.imwrite(os.path.join(visualPath,rank[0:39]+'.jpg'),combined)
        #t5=time.time()

        #t=t5-t1
        #print '%.2f %.2f %.2f %.2f' % ((t2-t1)/t,(t3-t2)/t,(t4-t3)/t,(t5-t4)/t)

#visualize(resultPath,queryPath,dataPath,visualPath,img_suffix,ids,n)

print '[Initialize multiprocessing]'
query_list = os.listdir(os.path.join(resultPath,'rankFiles'))
querynum = len(query_list)
print querynum	
tasks = []
proc_count = mtp.cpu_count() - 10
proc_max = 100
if proc_count > proc_max:
    proc_count = proc_max
block = int(math.ceil(querynum*1.0/proc_count))
box = []
print ' - process: ', proc_count
print ' - block size: ', block
for i in range(proc_count):
    left = int(i * block)
    if (i + 1) * block > querynum:
        right = querynum
    else: 
        right = int((i+1) * block)
    box.append([query_list[left:right]])
count = mtp.Value('i',0)
lock=mtp.Lock()

print '[ visualize start]'
duration =  time.time()
for i in range(proc_count):
    proc = mtp.Process(target=visualize, args=(i,lock,count,box[i][0],queryPath,dataPath,visualPath,img_suffix,ids))
    proc.start()
    tasks.append(proc)

for proc in tasks:
    proc.join()

duration = time.time() - duration
print 'visualize time: ',int(duration), 's'

