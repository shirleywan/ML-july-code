import os
import sys
import numpy as np
import cv2
import time

galleryPath1 = os.path.join(sys.argv[1],'gallery')
queryPath1   = os.path.join(sys.argv[1],'query')
galleryPath2 = os.path.join(sys.argv[2],'gallery')
queryPath2   = os.path.join(sys.argv[2],'query')
savePath = sys.argv[3]
resultPath1 = os.path.join(sys.argv[4] , 'rankFiles')
resultPath2 = os.path.join(sys.argv[5] , 'rankFiles')

print "queryPath1: "  , queryPath1
print "galleryPath1: ", galleryPath1
print "queryPath2: "  , queryPath2
print "galleryPath2: ", galleryPath2
print "resultPath1: ", resultPath1
print "resultPath2: ", resultPath2

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

id_location = 4 # same camera take one pic
cam_location = 4
n = 0
query_txt1 = os.listdir(resultPath1) #first dictionary,made up a list
query_txt2 = os.listdir(resultPath2)
query_txt1 = sorted(query_txt1)
query_txt2 = sorted(query_txt2)
query_txt_list = [query_txt1 , query_txt2]
print "query1: " , len(query_txt1)
print "query2: " , len(query_txt2)

ids1={}
for line in open(galleryPath1+'.list').readlines():
    id='_'.join(line.split('_')[:id_location])
    cam=line.split('_')[cam_location]
    if id not in ids1.keys():
        ids1[id]={}
    if cam not in ids1[id].keys():
        ids1[id][cam]=[]
    ids1[id][cam].append(line[:-1])

ids2={} #
for line in open(galleryPath2+'.list').readlines():
    id='_'.join(line.split('_')[:id_location])
    cam=line.split('_')[cam_location]
    if id not in ids2.keys():
        ids2[id]={}
    if cam not in ids2[id].keys():
        ids2[id][cam]=[]
    ids2[id][cam].append(line[:-1])

for k in range(len(query_txt_list[0])):
    top10_onequery = [0, 0]
    if n %100 == 0:
        print 'Visualized: ', n
    n += 1
    for j in range(2):
        rank = query_txt_list[j][k] #the kth filename
        if j == 0:
            combined_last=np.zeros((0,21*96,3))
            combined = np.zeros((192,0,3))
            gtBar=np.zeros((192,96,3))
            rank_name = rank.split('.')[0] #img name
            org=cv2.imread(os.path.join(queryPath1,rank_name +'.jpg')) #find query1 path
            if org is None:
                print 'no photo: '+os.path.join(queryPath1,rank.split('.')[0]+'.jpg')
                continue
            org=cv2.resize(org,(96,192))

            combined = np.append(combined, org, axis=1)  # find to combined
            rankFile = open(os.path.join(resultPath1, rank)).readlines()
            # id=rank[0:28]
            id = '_'.join(rank.split('_')[:id_location])  # find id
            
            if id not in ids1.keys():
                print 'the query is not in the gallery'
                continue
            total_num = 0
            for cam in ids1[id].keys():
                img=cv2.imread(os.path.join(galleryPath1,ids1[id][cam][0]))
                if img is None:
                    print 'the image in None'
                img = cv2.resize(img,(96,192))
                label = cam
                cv2.putText(img,label,(65,12),0,0.5,(255,255,255),3)
                cv2.putText(img,label,(65,12),0,0.5,(0,0,0),2)
                gtBar = np.append(gtBar , img , axis = 1)
                total_num += 1
            blackBar = np.zeros((192,96*(20-len(ids1[id].keys())),3))
            gtBar = np.append(gtBar , blackBar , axis=1)

            for i in xrange(20):
                # t31=time.time()
                # print rankFile[i]
                name = rankFile[i].split(' ')[0] + '.jpg'  # the ith pic
                # print name
                id2 = '_'.join(rankFile[i].split('_')[:id_location])
                img = cv2.imread(os.path.join(galleryPath1, name))  # from gallery get the img
                # t32=time.time()
                img = cv2.resize(img, (96, 192))
                #            if j == 0:
                #                img_mask = cv2.imread(os.path.join(maskPath, name.split('.')[0] + '.png'))
                #                img_mask = cv2.resize(img_mask, (96,192))
                #                img_mask = cv2.imread(os.path.join(maskPath, name.split('.')[0] + '.png'))
                #                img_mask = cv2.resize(img_mask, (96,192))
                #                img = img * img_mask
                # t33=time.time()
                label = 'x'
                color = (0, 0, 255)
                # print cam
                # print id
                # print ids[id][cam]
                # print name
                for cam in ids1[id]:
                    if name in ids1[id][cam]:
                        label = 'o'
                        color = (60, 255, 60)
                        if (i + 1) <= 10:
                            top10_onequery[j] += 1
                        break
                # t34=time.time()
                # print label
                labelcam = rankFile[i].split('_')[cam_location]
                cv2.putText(img, label, (0, 12), 0, 0.8, color, 3)
                cv2.putText(img, labelcam, (75, 10), 0, 0.3, (255, 255, 255), 2)
                cv2.putText(img, labelcam, (75, 10), 0, 0.3, (0, 0, 0), 1)
                #combined = np.hstack((combined, img))
                combined = np.hstack((combined, img))
                # t35=time.time()
                # t30=t35-t31
                # print '%.2f %.2f %.2f %.2f' % ((t32-t31)/t30,(t33-t32)/t30,(t34-t33)/t30,(t35-t34)/t30)
                # t4=time.time()
            print 'combined shape: ', combined.shape
            print 'gtBar: ',gtBar.shape
            combined = np.append(combined, gtBar, axis=0)
            combined_last = np.vstack((combined_last, combined))

        if j == 1:
            # combined_last=np.zeros((0,21*96,3))
            combined = np.zeros((192,0,3))
            gtBar=np.zeros((192,96,3))
            rank_name = rank.split('.')[0] #img name
            org=cv2.imread(os.path.join(queryPath2,rank_name +'.jpg')) #find query1 path
            if org is None:
                print 'no photo: '+os.path.join(queryPath2,rank.split('.')[0]+'.jpg')
                continue
            org=cv2.resize(org,(96,192))

            combined = np.append(combined, org, axis=1)  # find to combined
            rankFile = open(os.path.join(resultPath1, rank)).readlines()
            # id=rank[0:28]
            id = '_'.join(rank.split('_')[:id_location])  # find id

            if id not in ids2.keys():
                print 'the query is not in the gallery'
                continue
            total_num = 0
            for cam in ids2[id].keys():
                img=cv2.imread(os.path.join(galleryPath2,ids2[id][cam][0]))
                if img is None:
                    print 'the image in None'
                img = cv2.resize(img,(96,192))
                label = cam
                cv2.putText(img,label,(65,12),0,0.5,(255,255,255),3)
                cv2.putText(img,label,(65,12),0,0.5,(0,0,0),2)
                gtBar = np.append(gtBar , img , axis = 1)
                total_num += 1
            blackBar = np.zeros((192,96*(20-len(ids2[id].keys())),3))
            gtBar = np.append(gtBar , blackBar , axis=1)

            for i in xrange(20):
                # t31=time.time()
                # print rankFile[i]
                name = rankFile[i].split(' ')[0] + '.jpg'  # the ith pic
                # print name
                id2 = '_'.join(rankFile[i].split('_')[:id_location])
                img = cv2.imread(os.path.join(galleryPath2, name))  # from gallery get the img
                # t32=time.time()
                img = cv2.resize(img, (96, 192))
                #            if j == 0:
                #                img_mask = cv2.imread(os.path.join(maskPath, name.split('.')[0] + '.png'))
                #                img_mask = cv2.resize(img_mask, (96,192))
                #                img = img * img_mask
                # t33=time.time()
                label = 'x'
                color = (0, 0, 255)
                # print cam
                # print id
                # print ids[id][cam]
                # print name
                for cam in ids2[id]:
                    if name in ids2[id][cam]:
                        label = 'o'
                        color = (60, 255, 60)
                        if (i + 1) <= 10:
                            top10_onequery[j] += 1
                        break
                # t34=time.time()
                # print label
                labelcam = rankFile[i].split('_')[cam_location]
                cv2.putText(img, label, (0, 12), 0, 0.8, color, 3)
                cv2.putText(img, labelcam, (75, 10), 0, 0.3, (255, 255, 255), 2)
                cv2.putText(img, labelcam, (75, 10), 0, 0.3, (0, 0, 0), 1)
                combined = np.hstack((combined, img))
                # t35=time.time()
                # t30=t35-t31
                # print '%.2f %.2f %.2f %.2f' % ((t32-t31)/t30,(t33-t32)/t30,(t34-t33)/t30,(t35-t34)/t30)
                # t4=time.time()
            combined = np.append(combined, gtBar, axis=0)
            combined_last = np.vstack((combined_last, combined))
    print top10_onequery
    if top10_onequery[0] > top10_onequery[1]:
        save_label = 'good'
    elif top10_onequery[0] == top10_onequery[1]:
        save_label = 'equal'
    else:
        save_label = 'bad'
    point_pos = rank.find(".txt")
        # print os.path.join(visualPath,rank[0:point_pos]+'.jpg')
        # cv2.imwrite(os.path.join(visualPath, save_label, rank[0:point_pos] + '.jpg'), combined_last)
    cv2.imwrite(os.path.join(visualPath, rank[0:point_pos] + '.jpg'), combined_last)
