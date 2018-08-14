import os
import sys
import numpy as np
import cv2
import time

#n_full = 39  #41

dataPath=os.path.join(sys.argv[1], 'gallery')
maskPath = os.path.join(sys.argv[1], 'gallery_mask')
savePath=sys.argv[2]
queryPath=os.path.join(sys.argv[1], 'query')
querymaskPath = os.path.join(sys.argv[1], 'query_mask')
if not (os.path.isdir(maskPath) and os.path.isdir(querymaskPath)):
    print 'the testset has no mask'
    exit(0)
resultPath1=sys.argv[4]
resultPath2=sys.argv[5]
resultname1 = (resultPath1.split('/')[-2]).split('.')[-1]
resultname2 = (resultPath2.split('/')[-2]).split('.')[-1]
if resultname1 != resultname2:
    print 'the testset is different'
    exit(0)
resultPath_list = [resultPath1, resultPath2]

cam_location = 4
id_location = 4
print "dataPath: ", dataPath
print "savePath: ", savePath
print "queryPath: ", queryPath
#resnet
if not os.path.exists(savePath):
    savePath=savePath.split('/')
    savePath=os.path.join('/'.join(savePath[:-1]),'archive',savePath[-1])
    print savePath

if not os.path.exists(resultPath1):
    print 'No saved result found!'
    exit(0)
if not os.path.exists(resultPath2):
    print 'No saved result found!'
    exit(0)
visualPath=os.path.join(savePath,'compare_visual')
if not os.path.exists(visualPath):
    os.mkdir(visualPath)
visualEqual = os.path.join(visualPath, 'equal')
if not os.path.exists(visualEqual):
    os.mkdir(visualEqual)
visualGood = os.path.join(visualPath, 'good')
if not os.path.exists(visualGood):
    os.mkdir(visualGood)
visualBad = os.path.join(visualPath, 'bad')
if not os.path.exists(visualBad):
    os.mkdir(visualBad)

ids={}
for line in open(dataPath+'.list').readlines():
    id='_'.join(line.split('_')[:id_location])
    cam=line.split('_')[cam_location]
    if id not in ids.keys():
        ids[id]={}
    if cam not in ids[id].keys():
        ids[id][cam]=[]
    ids[id][cam].append(line[:-1])

n=0
query_txt1 = os.listdir(os.path.join(resultPath_list[0], 'rankFiles'))
query_txt2 = os.listdir(os.path.join(resultPath_list[1], 'rankFiles'))
query_txt_list = [query_txt1, query_txt2]
for k in range(len(query_txt1)):
    top10_onequery = [0, 0]
    if n %100 == 0:
        print 'Visualized: ', n
    n += 1
    for j in range(2):
        rank = query_txt_list[j][k]
        if j == 0:
            combined_last=np.zeros((0,21*96,3))
        combined = np.zeros((192,0,3))
        gtBar=np.zeros((192,96,3))
        rank_name = rank.split('.')[0]
        org=cv2.imread(os.path.join(queryPath,rank_name +'.jpg'))
        if org is None:
            print 'hello'
            print os.path.join(queryPath,rank.split('.')[0]+'.jpg')
            continue
        org=cv2.resize(org,(96,192))
        if j == 0:
            org_mask = cv2.imread(os.path.join(querymaskPath, rank_name + '.png'))
            org_mask = cv2.resize(org_mask, (96,192))
            org = org * org_mask
        combined=np.append(combined,org,axis=1)

        rankFile=open(os.path.join(resultPath_list[j],'rankFiles',rank)).readlines()
        #id=rank[0:28]
        id='_'.join(rank.split('_')[:id_location])   #t2=time.time()
        if id not in ids.keys():
            print "the query is not in the gallery"
            continue
        total_num = 0
        for cam in ids[id].keys():
            #print os.path.join(dataPath, ids[id][cam][0][:-1])
            #print os.path.exists(os.path.join(dataPath, ids[id][cam][0][:-1]))
            img=cv2.imread(os.path.join(dataPath,ids[id][cam][0]))
            if img is None:
                print 'the image in None'
            img=cv2.resize(img,(96,192))
            if j == 0:
                img_mask = cv2.imread(os.path.join(maskPath, ids[id][cam][0].split('.')[0] + '.png')) 
                img_mask = cv2.resize(img_mask,(96,192))
                img = img * img_mask 
            label=cam
            cv2.putText(img,label,(65,12),0,0.5,(255,255,255),3)
            cv2.putText(img,label,(65,12),0,0.5,(0,0,0),2)
            gtBar=np.append(gtBar,img,axis=1)
            total_num += 1
        blackBar=np.zeros((192,96*(20-len(ids[id].keys())),3))
        gtBar=np.append(gtBar,blackBar,axis=1)
        #t3=time.time()
        for i in xrange(20) :
            #t31=time.time()
            #print rankFile[i]
            name=rankFile[i].split(' ')[0] + '.jpg'
            #print name
            id2='_'.join(rankFile[i].split('_')[:id_location])
            img=cv2.imread(os.path.join(dataPath,name))
            #t32=time.time()
            img=cv2.resize(img,(96,192))
            if j == 0:
                img_mask = cv2.imread(os.path.join(maskPath, name.split('.')[0] + '.png'))
                img_mask = cv2.resize(img_mask, (96,192))
                img = img * img_mask
            #t33=time.time()
            label='x'
            color = (0,0,255)
            #print cam
            #print id
            #print ids[id][cam]
            #print name
            for cam in ids[id]:
                if name in ids[id][cam]:
                    label='o'
                    color=(60,255,60)
                    if (i+1) <= 10:
                        top10_onequery[j] += 1
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
        combined_last = np.vstack((combined_last, combined))
    print top10_onequery
    if top10_onequery[0] > top10_onequery[1]:
        save_label = 'good'
    elif top10_onequery[0] == top10_onequery[1]:
        save_label = 'equal'
    else:
        save_label = 'bad'
    point_pos=rank.find(".txt")
        #print os.path.join(visualPath,rank[0:point_pos]+'.jpg')
    cv2.imwrite(os.path.join(visualPath,save_label,rank[0:point_pos]+'.jpg'),combined_last)
	#cv2.imwrite(os.path.join(visualPath,rank[0:39]+'.jpg'),combined)
        #t5=time.time()

        #t=t5-t1
        #print '%.2f %.2f %.2f %.2f' % ((t2-t1)/t,(t3-t2)/t,(t4-t3)/t,(t5-t4)/t)



