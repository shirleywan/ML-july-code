from PIL import Image
import cv2
import numpy as np 
import os.path
#from skimage import io,data
import imghdr
import shutil
import multiprocessing as mtp
import math
import logging
import time

ext1 = 'jpg'
ext2 = 'png'

def getMultiImg(imgPath,maskPath,rgbMskPath,img_list):
	i = 0
	for filename in img_list:
		print filename
		#if filename[-3:]!=ext2:
			#continue
		i += 1
		print i
		if i%2000==0:
			print i
		imgName = filename[:-3] + ext1
		ori_mskImg = cv2.imread(os.path.join(maskPath,filename))
		png_name = filename[:-3]+ext2
		#cv2.imwrite(os.path.join(maskPath,png_name),ori_mskImg)
		mskImg=cv2.imread(os.path.join(maskPath,png_name))
		if mskImg.shape[0]!= 0:
			if os.path.isfile(os.path.join(imgPath,imgName)):
				rgbImg = cv2.imread(os.path.join(imgPath,imgName))
#				print rgbImg.shape
#				print mskImg.shape
				mskImg = cv2.resize(mskImg,(rgbImg.shape[1],rgbImg.shape[0]))
				for c in range(mskImg.shape[0]):
					for l in range(mskImg.shape[1]):
						if (mskImg[c,l]-[0,0,0]).any():
#							print mskImg[c,l] 
							mskImg[c,l][0] = 255
#							print mskImg[c,l]
						else:
							mskImg[c,l][0] = 0
				rgbImg = np.array(rgbImg)  
				mskImg = np.array(mskImg)  
				rgbd = np.zeros((np.size(rgbImg,0),np.size(rgbImg,1),4),dtype=np.uint8)  
				rgbd[:, :, 0] = rgbImg[:, :, 0]  
				rgbd[:, :, 1] = rgbImg[:, :, 1]  
				rgbd[:, :, 2] = rgbImg[:, :, 2]  
				rgbd[:, :, 3] = mskImg[:, :, 0]
#				print rgbd.shape
				filename = filename[:-3] + ext2
    				cv2.imwrite(os.path.join(rgbMskPath,filename), rgbd)  
#				tmp = cv2.imread(os.path.join(rgbMskPath,filename),-1)
#				print tmp.shape
					

def checkPath(dir1):
	if not os.path.exists(dir1):
		os.makedirs(dir1)

def multiCombine(dir1,dir2,dir3):
	print "imgPath:",dir1
	print "mskPath:",dir2
	print "rgbMskPath:",dir3
	img_list = os.listdir(dir2)
	img_num = len(img_list)
	tasks = []
	proc_count = mtp.cpu_count()-10
	block = int(math.ceil(img_num*1.0/proc_count))
	box = []
	print ' - Process:',proc_count
	print ' - Block size:',block
	for i in range(proc_count):
		left = int(i*block)
		if (i+1)*block > img_num:
			right = int(img_num)
		else:
			right = int((i+1)*block)
		box.append(img_list[left:right])
	tgtFunc = getMultiImg
	count = mtp.Value('i', 0)
	lock = mtp.Lock()

	print '4channel generation start'
	duration = time.time()
	for i in range(proc_count):
		proc = mtp.Process(target=tgtFunc, args=(dir1,dir2,dir3,box[i]))
		proc.start()
		tasks.append(proc)

	for proc in tasks:
		proc.join()

	duration = time.time() - duration
	print 'Combining duration:', int(duration), 's'

if __name__ == '__main__':
#	rootPath = '/home/lixiaoli/multiModel_mask/testImgs'
#	rootPath = '/home/lixiaoli/multiModel_mask/data_origin'
#	rootPath = '/home/lixiaoli/multiModel_mask/select-plus'
#	rgbPath = os.path.join(rootPath,'rgb')
#	mskPath = os.path.join(rootPath,'msk')
#	rgbMskPath = os.path.join(rootPath,'rgb_msk_256')
#	checkPath(rgbMskPath)
#	getMultiImg(rgbPath,mskPath,rgbMskPath th = '/home/cuiqiangqiang/data/testset/DM_test_new/query'
        rgbPath = '/home/data1/KakoData/Patch_ALL_20180630_Kakou_new_train_test/gallery'
        mskPath = '/home/miaojiaxu/K-Ped-test/gallery'
        rgbMskPath = '/home/miaojiaxu/4chnl-test/K-Ped-test/gallery'
        checkPath(rgbMskPath)
        multiCombine(rgbPath,mskPath,rgbMskPath)
'''	
	rgbPath = '/home/data1/Yiganduotou-Person/updateAll_scenes-20180702/test/query'
        mskPath = '/home/miaojiaxu/K-Ped-5on1-test/query'
        rgbMskPath = '/home/miaojiaxu/4chnl-test/K-Ped-5on1-test/query'
        checkPath(rgbMskPath)
        multiCombine(rgbPath,mskPath,rgbMskPath)
	rgbPath = '/home/data1/Yiganduotou-Person/updateAll_scenes-20180702/test/gallery'
        mskPath = '/home/miaojiaxu/K-Ped-5on1-test/gallery'
        rgbMskPath = '/home/miaojiaxu/4chnl-test/K-Ped-5on1-test/gallery'
        checkPath(rgbMskPath)
        multiCombine(rgbPath,mskPath,rgbMskPath)
	rgbPath = '/home/data1/KakoData/Patch_ALL_20180630_Kakou_new_train_test/query'
        mskPath = '/home/miaojiaxu/K-Ped-test/query'
        rgbMskPath = '/home/miaojiaxu/4chnl-test/K-Ped-test/query'
        checkPath(rgbMskPath)
        multiCombine(rgbPath,mskPath,rgbMskPath)

	rgbPath = '/home/data1/KakoData/Patch_ALL_20180630_Kakou_new_train_test/gallery'
        mskPath = '/home/miaojiaxu/K-Ped-test/gallery'
        rgbMskPath = '/home/miaojiaxu/4chnl-test/K-Ped-test/gallery'
        checkPath(rgbMskPath)
        multiCombine(rgbPath,mskPath,rgbMskPath)

	rgbPath = '/home/miaojiaxu/occ_testset/query'
        mskPath = '/home/miaojiaxu/occ-test/query'
        rgbMskPath = '/home/miaojiaxu/4chnl-test/occ_test/query'
        checkPath(rgbMskPath)
        multiCombine(rgbPath,mskPath,rgbMskPath)
	rgbPath = '/home/miaojiaxu/occ_testset/gallery'
        mskPath = '/home/miaojiaxu/occ-test/gallery'
        rgbMskPath = '/home/miaojiaxu/4chnl-test/occ_test/gallery'
        checkPath(rgbMskPath)
        multiCombine(rgbPath,mskPath,rgbMskPath)

	rgbPath = '/home/liguangrui/data/testset/select_plus_new/query'
        mskPath = '/home/liguangrui/data/mask-test/select_plus_new/query'
        rgbMskPath = '/home/liguangrui/data/4chnl-test/select_plus_new/query'
        checkPath(rgbMskPath)
        multiCombine(rgbPath,mskPath,rgbMskPath)
	rgbPath = '/home/liguangrui/data/testset/select_plus_new/gallery'
        mskPath = '/home/liguangrui/data/mask-test/select_plus_new/gallery'
        rgbMskPath = '/home/liguangrui/data/4chnl-test/select_plus_new/gallery'
        checkPath(rgbMskPath)
        multiCombine(rgbPath,mskPath,rgbMskPath)
     
	
	rgbPath = '/home/lixiaoli/multiModel_mask/data-laohu/select_plus_complex-BG/gallery'
	mskPath = '/home/lixiaoli/multiModel_mask/data-laohu/select_plus-mask/mask-gallery'
	rgbMskPath = '/home/lixiaoli/multiModel_mask/data-laohu/select_plus_rgbOriMsk/gallery'
	checkPath(rgbMskPath)
	getMultiImg(rgbPath,mskPath,rgbMskPath)

	rgbPath = '/home/lixiaoli/multiModel_mask/data-laohu/select_plus_complex-BG/query'
	mskPath = '/home/lixiaoli/multiModel_mask/data-laohu/select_plus-mask/mask-query'
	rgbMskPath = '/home/lixiaoli/multiModel_mask/data-laohu/select_plus_rgbOriMsk/query'
        checkPath(rgbMskPath)
        getMultiImg(rgbPath,mskPath,rgbMskPath)

	rgbPath = '/home/lixiaoli/multiModel_mask/data-laohu/select_plus_complex-BG/gallery'
        mskPath = '/home/lixiaoli/multiModel_mask/data-laohu/select_plus_complex-BG-mask/mask-gallery'
	rgbMskPath = '/home/lixiaoli/multiModel_mask/data-laohu/select_plus_complex-BG_rgbMsk/gallery'
        checkPath(rgbMskPath)
        getMultiImg(rgbPath,mskPath,rgbMskPath)

	rgbPath = '/home/lixiaoli/multiModel_mask/data-laohu/select_plus_complex-BG/query'
        mskPath = '/home/lixiaoli/multiModel_mask/data-laohu/select_plus_complex-BG-mask/mask-query'
	rgbMskPath = '/home/lixiaoli/multiModel_mask/data-laohu/select_plus_complex-BG_rgbMsk/query'
        checkPath(rgbMskPath)
        getMultiImg(rgbPath,mskPath,rgbMskPath)
'''

