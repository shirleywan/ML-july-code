import sys
import os
import numpy as np
import time
import math
import multiprocessing as mtp
from numpy import *
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s : %(message)s')
#mjx

def extract_id(name):
    return '_'.join(name.split('_')[:5])

def full_name(name):
    return name.split('.')[0]

#############
#n_cam=34
#n_full=90
keyFeatures=[]

def L1(keyFeature, queryFeature):
    return linalg.norm(keyFeature - queryFeature,ord=1)

def L2(keyFeature, queryFeature):
    return linalg.norm(keyFeature - queryFeature,ord=2)

def cos(keyFeature, queryFeature):
    return keyFeature.dot(queryFeature)

def HM(keyFeature, queryFeature):
    return np.count_nonzero(np.array(keyFeature)!=np.array(queryFeature))

def Normalize(features):
    for i in range(len(features)):
        features[i]=features[i]/np.sqrt(features[i].dot(features[i]))
    return features

def Sigmoid(features):
    return 1/(1+np.exp(np.negative(features)))

def Hash(features):
    return (features>0.99)*1





def query_process_desc(proc,lock,count,queryFeatures, queryNames, keyNames, saveDir,distFunc,d_limit,topN):
    global keyFeatures
    for queryFeature,queryName in zip(queryFeatures,queryNames):
        queryID = extract_id(queryName)
        topR=[]
        maxName=''
        maxDist=d_limit
        for i in xrange(len(keyNames)):
            keyID=extract_id(keyNames[i])
            if keyID!= queryID:
                d=distFunc(keyFeatures[i],queryFeature)
                maxID=extract_id(maxName)
                # compare dist in the group with same ID
                if keyID==maxID:
                    if d>maxDist:
                        maxName=keyNames[i]
                        maxDist=d
                else:
                    # save previous maximum distance and name
                    topR.append([full_name(maxName),maxDist])
                    # reset maxName and maxDist for new ID
                    maxName=keyNames[i]
                    maxDist=d
        topR.append([maxName.split('.')[0],maxDist])
        topR_sorted= sorted(topR, key=lambda d:d[1],reverse=True)

        k=0
        w_file = open(saveDir+'/' + full_name(queryName)+'.txt', 'w')
        for line in topR_sorted:
            if k<topN:
                w_file.write(line[0]+" " + str(line[1]) + "\n")
                k+=1

        w_file.close()
        lock.acquire()
        count.value +=1
        lock.release()
        if count.value % 100 == 0:
            logging.info(str(count.value) + " query finished")

def query_process_asc(proc,lock,count,queryFeatures, queryNames, keyNames, saveDir,distFunc,d_limit,topN):
    global keyFeatures
    for queryFeature,queryName in zip(queryFeatures,queryNames):
        queryID = extract_id(queryName)
        topR=[]
        minName=''
        minDist=d_limit
        for i in xrange(len(keyNames)):
            keyID=extract_id(keyNames[i])
            if keyID!= queryID:
                d=distFunc(keyFeatures[i],queryFeature)
                minID=extract_id(minName)
                # compare dist in the group with same ID
                if keyID==minID:
                    if d<minDist:
                        minName=keyNames[i]
                        minDist=d
                else:
                    # save previous minimum distance and name
                    topR.append([minName,minDist])
                    # reset minName and minDist for new ID
                    minName=keyNames[i]
                    minDist=d
        topR.append([full_name(minName),minDist])         
        topR_sorted= sorted(topR, key=lambda d:d[1])

        k=0
        w_file = open(saveDir+'/' + full_name(queryName)+'.txt', 'w')
        for line in topR_sorted:
            if k<topN:
                w_file.write(line[0]+" " + str(line[1]) + "\n")
                k+=1

        w_file.close()
        lock.acquire()
        count.value +=1
        lock.release()
        if count.value % 100 == 0:
            logging.info(str(count.value) + " query finished")

def query_process_hash(proc,lock,count,queryFeatures, queryNames, keyNames, saveDir,distFunc,d_limit,topN):
    global keyFeatures
    for queryFeature,queryName in zip(queryFeatures,queryNames):
        queryID = extract_id(queryName)
        topR={}
        minName=''
        minDist=d_limit
        for i in range(len(keyNames)):
            keyID=extract_id(keyNames[i])
            if keyID!= queryID:
                d=distFunc(keyFeatures[i],queryFeature)
                minID=extract_id(minName)
                # compare dist in the group with same ID
                if keyID==minID:
                    if d<minDist:
                        minName=keyNames[i]
                        minDist=d
                else:
                    # save previous minimum distance and name
                    if minDist not in topR:
                        topR[minDist]=[]
                    topR[minDist].append(full_name(minName))
                    # reset minName and minDist for new ID
                    minName=keyNames[i]
                    minDist=d
        if minDist not in topR:
            topR[minDist]=[]
        topR[minDist].append(full_name(minName))

        k=0
        w_file = open(saveDir+'/' + full_name(queryName)+'.txt', 'w')
        del topR[d_limit]
        for i in sorted(topR):
            for line in topR[i]:
                if k<topN:
                    w_file.write(line+" " + str(i) + "\n")
                    k+=1

        w_file.close()
        lock.acquire()
        count.value +=1
        lock.release()
        if count.value % 100 == 0:
            logging.info(str(count.value) + " query finished")

def query(extraFEATs,galleryFEATs,queryFEATs,extraList,galleryList,queryList,saveDir,dims,isNorm,isSig,isHash,distance,topN,proc_max):
    print '[ Load features ]'
    extras = np.fromfile(extraFEATs, dtype = 'float32')
    print ' - Extra loaded:',len(extras)/dims
    gallerys = np.fromfile(galleryFEATs, dtype = 'float32')
    print ' - Gallery loaded:',len(gallerys)/dims
    keys= np.concatenate((gallerys,extras))
    global keyFeatures
    keyFeatures = keys.reshape((len(keys)/dims, dims))
    print ' - Combined keys:',keyFeatures.shape[0]
    queryFile = np.fromfile(queryFEATs, dtype = 'float32')
    queryFeatures = queryFile.reshape((len(queryFile)/dims, dims))
    print ' - Query loaded:',queryFeatures.shape[0]
    
    extraNames=open(extraList).readlines()
    print ' - Extra list:',len(extraNames)
    galleryNames=open(galleryList).readlines()
    print ' - Gallery list:',len(galleryNames)
    keyNames=galleryNames
    keyNames.extend(extraNames)
    print ' - Combined key list:',len(keyNames)
    queryNames=open(queryList).readlines()
    print ' - Query list:',len(queryNames)
    print ''

    print '[ Normalize ]',isNorm==1
    if isNorm==1:
        keyFeatures=Normalize(keyFeatures)
        queryFeatures=Normalize(queryFeatures)
    print ''

    print '[ Sigmoid ]',isSig==1
    if isSig==1:
        keyFeatures=Sigmoid(keyFeatures)
        queryFeatures=Sigmoid(queryFeatures)
    print ''

    print '[ Hash ]',isHash==1
    if isHash==1:
        keyFeatures=Hash(keyFeatures)
        queryFeatures=Hash(queryFeatures)
    print ''

    print '[ Distance ]',distance
    procFunc=query_process_asc
    d_limit=0xffffffff
    if distance=='L1':
        distFunc=L1
    elif distance=='L2':
        distFunc=L2
    elif distance=='cos':
        distFunc=cos
        procFunc=query_process_desc
        d_limit=-1
    elif distance=='Hamming':
        distFunc=HM
        procFunc=query_process_hash
        d_limit=dims
        
    else:
        print 'No such distance defined: ',distance
        exit(0)
    print ''

    print '[ Initialize multiprocessing ]'
    tasks=[]
    proc_count=mtp.cpu_count()- 15
    if proc_count>proc_max:
        proc_count=proc_max
    block=int(math.ceil(len(queryFeatures)*1.0/proc_count))
    box=[]
    print ' - Process:',proc_count
    print ' - Block size:',block
    for i in range(proc_count):
        left=int(i*block)
        if (i+1)*block > len(queryFeatures):
            right=int(len(queryFeatures))
        else:
            right=int((i+1)*block)
        box.append([queryFeatures[left:right],queryNames[left:right]])
    
    count=mtp.Value('i',0)
    lock=mtp.Lock()
    print ''

    print '[ Query start ]'
    duration=time.time()
    for i in range(proc_count):
        proc=mtp.Process(target=procFunc, args=(i,lock,count,box[i][0],box[i][1],keyNames,saveDir,distFunc,d_limit,topN))
        proc.start()
        tasks.append(proc)

    for proc in tasks:
        proc.join()

    duration=time.time()-duration
    print 'Query duration:',int(duration),'s'
    

if __name__=='__main__':
    query(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7],int(sys.argv[8]),int(sys.argv[9]),int(sys.argv[10]),int(sys.argv[11]),sys.argv[12],int(sys.argv[13]),int(sys.argv[14]))
