from __future__ import division
import sys
import os
import shutil
import math
import time
import numpy as np
import multiprocessing as mtp

#n_id=30 #28
#n_cam=34 #32
def extract_id(name):
    return '_'.join(name.split('_')[:4])

def extract_cam(name):
    return '_'.join(name.split('_')[:5])

def camid(name):
    return name.split('_')[4]


###############
def getTotalRecall(galleryNames,queryName):
        queryName_id =extract_id(queryName)
        queryName_cam = extract_cam(queryName)
        queryCamID = camid(queryName)
        gtList = {}
        for galleryName in galleryNames:
                gallery_id = extract_id(galleryName)
                gallery_cam = extract_cam(galleryName)
                camID = camid(galleryName)
                if(queryName_id == gallery_id) and (camID != queryCamID):
                        gtList[gallery_cam] = 1
        return len(gtList)


def rank_thread(lock,total,count,file_count,m_top1,m_top3,m_top5,m_top10,m_top50,m_top100,m_topn1,m_topn2,n1,n2,rankFiles, rankFilePath,keyNames,galleryNames,t_top1,t_top3,t_top5,t_top10,t_top50,t_top100,t_topn1,t_topn2):
    for rankFile in rankFiles:
        lock.acquire()
        count.value+=1
        tem=count.value
        lock.release()
        if count.value % 100 == 0:
            local=time.asctime( time.localtime(time.time()))
            print '['+local+'] RANK: '+str(tem)+' of '+str(file_count)
        
        n=getTotalRecall(galleryNames,rankFile)
        if n==0:
            total.value-=1
            continue

        r_file=open(os.path.join(rankFilePath,rankFile))
        r_lines=r_file.readlines()
        i=0
        t3=t5=t10=t50=t100=tn1=tn2=0
	if extract_id(rankFile)==extract_id(r_lines[0]):
           
            lock.acquire()
            m_top1.value+=1
            lock.release()
        for line in r_lines:
            if extract_id(rankFile)==extract_id(line):
                if i<3:
                    t3+=1
                if i<5:
                    t5+=1
                if i<10:
                    t10+=1
                if i<50:
                    t50+=1
                if i<100:
                    t100+=1
		if i<n1:
		    tn1+=1
		if i<n2:
		    tn2+=1
            i+=1
        r_file.close()
        
        lock.acquire()
        m_top3.value+=t3/n
        m_top5.value+=t5/n
        m_top10.value+=t10/n
        m_top50.value+=t50/n
        m_top100.value+=t100/n
	m_topn1.value+=tn1/n
	m_topn2.value+=tn2/n
        
        t_top3.value+=t3/min(n,3)
        t_top5.value+=t5/min(n,5)
        t_top10.value+=t10/min(n,10)
        t_top50.value+=t50/min(n,50)
        t_top100.value+=t100/min(n,100)
	t_topn1.value+=tn1/min(n,n1)
	t_topn2.value+=tn2/min(n,n2)
        
        lock.release()


def rank(testPlace, saveName, extraList, galleryList, n1, n2):
    rankFilePath=os.path.join(testPlace,saveName,'rankFiles')
    rankFiles= os.listdir(rankFilePath)
    file_count=len(rankFiles)

    tasks=[]
    proc_count=mtp.cpu_count()-1
    block=math.ceil(len(rankFiles)*1.0/proc_count)
    box=[]
    for i in range(proc_count):
        left=int(i*block)
        if (i+1)*block > len(rankFiles):
            right=int(len(rankFiles))
        else:
            right=int((i+1)*block)
        box.append(rankFiles[left:right])

    extraNames = open(extraList).readlines()
    galleryNames = open(galleryList).readlines()
    keyNames = galleryNames
    keyNames.extend(extraNames)

    m_top1=mtp.Value('f',0.0)
    
    m_top3=mtp.Value('f',0.0)
    m_top5=mtp.Value('f',0.0)
    m_top10=mtp.Value('f',0.0)
    m_top50=mtp.Value('f',0.0)
    m_top100=mtp.Value('f',0.0)
    m_topn1=mtp.Value('f',0.0)
    m_topn2=mtp.Value('f',0.0)
    
    t_top3=mtp.Value('f',0.0)
    t_top5=mtp.Value('f',0.0)
    t_top10=mtp.Value('f',0.0)
    t_top50=mtp.Value('f',0.0)
    t_top100=mtp.Value('f',0.0)
    t_topn1=mtp.Value('f',0.0)
    t_topn2=mtp.Value('f',0.0)
    total=mtp.Value('i',len(rankFiles))
    count=mtp.Value('i',0)
    lock=mtp.Lock()
    for i in range(proc_count):
        proc = mtp.Process(target=rank_thread, args=(lock,total,count,file_count,m_top1,m_top3,m_top5,m_top10,m_top50,m_top100,m_topn1,m_topn2,n1,n2, box[i],rankFilePath,keyNames,galleryNames,t_top3,t_top3,t_top5,t_top10,t_top50,t_top100,t_topn1,t_topn2))
        proc.start()
        tasks.append(proc)
    
    for proc in tasks:
        proc.join()

    top1=m_top1.value/total.value
    
    top3=m_top3.value/total.value
    top5=m_top5.value/total.value
    top10=m_top10.value/total.value
    top50=m_top50.value/total.value
    top100=m_top100.value/total.value
    topn1=m_topn1.value/total.value
    topn2=m_topn2.value/total.value

    t_top1=m_top1.value/total.value
    
    t_top3=t_top3.value/total.value
    t_top5=t_top5.value/total.value
    t_top10=t_top10.value/total.value
    t_top50=t_top50.value/total.value
    t_top100=t_top100.value/total.value
    t_topn1=t_topn1.value/total.value
    t_topn2=t_topn2.value/total.value

    summary=open(os.path.join(testPlace,saveName,'summary.txt'),'w')
    summary.write('rank 1\t\ttop 3\t\ttop5\t\ttop 10\t\ttop 50\t\ttop 100\t\ttop%d\t\ttop%d\n' % (n1,n2))
    summary.write('%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%6f' % (top1,top3,top5,top10,top50,top100,topn1,topn2))
    summary.write('rank 1\t\ttop 3\t\ttop5\t\ttop 10\t\ttop 50\t\ttop 100\t\ttop%d\t\ttop%d\n' % (n1,n2))
    summary.write('%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%6f' % (t_top1,t_top3,t_top5,t_top10,t_top50,t_top100,t_topn1,t_topn2))
    summary.close()
    print ''
    print '------------------------- RESULT -----------------------------------'
    print 'rank 1    top 3    top5    top 10   top 50   top 100  top%d   top%d' % (n1,n2)
    print '%.6f %.6f %.6f %.6f %.6f %.6f %.6f %.6f' % (top1,top3,top5,top10,top50,top100,topn1,topn2)
    print '--------------------------------------------------------------------'   

    print ''
    print ''
    print '------------------------- RESULT -----------------------------------'
    print 'rank 1    top 3    top5    top 10   top 50   top 100  top%d   top%d' % (n1,n2)
    print '%.6f %.6f %.6f %.6f %.6f %.6f %.6f %.6f' % (t_top1,t_top3,t_top5,t_top10,t_top50,t_top100,t_topn1,t_topn2)
    print '--------------------------------------------------------------------'   

    print ''
    archive=raw_input('Options: [A]rchive, [D]elete, [K]eep\n')
    while archive.lower() not in ['a','d','k']:
	archive=raw_input('Invalid input, retry:\n')
    if archive.lower()=='a':
	shutil.move(os.path.join(testPlace,saveName),os.path.join(testPlace,'archive'))
	print 'Archived:',os.path.abspath(os.path.join(testPlace,'archive',saveName))
    if archive.lower()=='d':
	if saveName[0:6]=='result':
            os.system('rm -rf '+os.path.join(testPlace,saveName))
            print 'Deleted:',os.path.join(testPlace,saveName)


if __name__=='__main__':
    rank(sys.argv[1],sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]), int(sys.argv[6]))
