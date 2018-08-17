import os
import sys
import numpy as np
import cv2
import time

n_full = 41 #39

dataPath=os.path.join(sys.argv[1],'gallery')
savePath=sys.argv[2]
queryPath=sys.argv[3]
resultPath=sys.argv[4]

print "dataPath: ", dataPath
print "savePath: ", savePath
print "queryPath: ", queryPath

if not os.path.exists(savePath):
    savePath=savePath.split('/')
    savePath=os.path.join('/'.join(savePath[:-1]),'archive',savePath[-1])

if not os.path.exists(savePath):
    print 'No saved result found!'
    exit(0)

visualPath=os.path.join(resultPath,'visual')
if not os.path.exists(visualPath):
    os.mkdir(visualPath)

ids={}
for line in open(dataPath+'.list').readlines():
    id=line[0:28]
    cam=line[0:32]
    if id not in ids:
        ids[id]={}
    if cam not in ids[id]:
        ids[id][cam]=[]
    ids[id][cam].append(line[0:n_full]+'.jpg')

n=0
for rank in os.listdir(os.path.join(resultPath,'rankFiles')):
    #t1=time.time()
    if n%100==0:
        print 'Visualized: ',n
    n+=1
    combined=np.zeros((192,0,3))
    gtBar=np.zeros((192,96,3))
    org=cv2.imread(os.path.join(queryPath,rank[0:n_full]+'.jpg'))
    if org is None:
        print os.path.join(queryPath,rank[0:n_full]+'.jpg')
        continue
    org=cv2.resize(org,(96,192))
    combined=np.append(combined,org,axis=1)

    rankFile=open(os.path.join(resultPath,'rankFiles',rank)).readlines()
    #id=rank[0:28]
    id=rank[0:7]+"201"+rank[10:28]    #t2=time.time()
    for cam in ids[id]:
        img=cv2.imread(os.path.join(dataPath,ids[id][cam][0]))
        img=cv2.resize(img,(96,192))
        label=cam[-3:]
        cv2.putText(img,label,(65,12),0,0.5,(255,255,255),3)
        cv2.putText(img,label,(65,12),0,0.5,(0,0,0),2)
        gtBar=np.append(gtBar,img,axis=1)
    blackBar=np.zeros((192,96*(20-len(ids[id])),3))
    gtBar=np.append(gtBar,blackBar,axis=1)
    #t3=time.time()
    for i in xrange(20) :
        #t31=time.time()
        name=rankFile[i][0:n_full]+'.jpg'
        id2=rankFile[i][0:28]
        img=cv2.imread(os.path.join(dataPath,rankFile[i][0:n_full]+'.jpg'))
        #t32=time.time()
        img=cv2.resize(img,(96,192))
        #t33=time.time()
        label='x'
        color=(0,0,255)
        for cam in ids[id]:
            if name in ids[id][cam]:
                label='o'
                color=(60,255,60)
                break
        #t34=time.time()
        labelcam=rankFile[i][29:32]
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
    print os.path.join(visualPath,rank[0:point_pos]+'.jpg')
    cv2.imwrite(os.path.join(visualPath,rank[0:point_pos]+'.jpg'),combined)
	#cv2.imwrite(os.path.join(visualPath,rank[0:39]+'.jpg'),combined)
    #t5=time.time()

    #t=t5-t1
    #print '%.2f %.2f %.2f %.2f' % ((t2-t1)/t,(t3-t2)/t,(t4-t3)/t,(t5-t4)/t)



