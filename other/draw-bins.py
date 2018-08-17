import os
from PIL import Image
from matplotlib import pyplot as plt
from collections import Counter
def draw_hist(path1):
	print path1
	filenames = os.listdir(path1)
	heiList = []
	ll = []
	img_num = 0
	for imgName in filenames:
		img_num += 1
#		if img_num%5000 == 0:
#			print 'img_num:',img_num
		img = Image.open(os.path.join(path1,imgName))
		heiList.append(img.size[1])
		ll.append(img.size[1]/100)
		#print img.size[1]
#	print 'img_num:',img_num
	dic = Counter(ll)
	print [(k,dic[k]) for k in sorted(dic.keys())]
	'''print ll	
	for k, g in itertools.groupby(ll):
		dic['{}-{}'.format(k*100+1, (k+1)*100)] = len(list(g))
		#print k,list(g)
	'''
#	print(path1)
	'''
  plt.hist(heiList,12)
	num = len(path1.split('/'))
	plt.grid(True, linestyle = "--", axis= "y", color = "r", linewidth = "1")  
	plt.title('_'.join(path1.split('/')[num-2:num]))
	img_name = '_'.join(path1.split('/')[num-3:num])
	plt.savefig('/home/lixiaoli/'+img_name+'.png')
	plt.show()
'''
if __name__ == '__main__':
	# path1 = '/home/data1/KakoData/Patch_ALL_20180630_Kakou'
	# draw_hist(path1)
	# path1 = '/home/data1/HY-Actor/class1'
	# draw_hist(path1)
	# path1 = '/home/data1/HY-Actor/class2'
    	# draw_hist(path1)
	# path1 = '/home/data1/HY-Actor/class3'
     #    draw_hist(path1)
	# path1 = '/home/data1/HY-Actor/class4'
     #    draw_hist(path1)
	# path1 = '/home/data1/BikeAll_new/train'
	# draw_hist(path1)
	path1 = 'G:\\nuoya-ped-kakou\\nuoya-ped-kakou-patch\\'
	draw_hist(path1)
	path1 = 'G:\\nuoya-fankakou\\nuoya-fankakou-patch\\'
	draw_hist(path1)
	path1 = 'G:\\meiti-kakou\\meiti-kakou-patch\\'
	draw_hist(path1)
	path1 = 'G:\\meiti-fankakou\\meiti-fankakou-patch-1\\'
	draw_hist(path1)
	# path1 = '/home/data1/HY-Actor/class4'
	# draw_hist(path1)
	# path1 = '/home/data1/BikeAll_new/train'
	# draw_hist(path1)

'''
	path1 = '/home/data1/Yiganduotou-Person/updateAll-20180702'
#        draw_hist(path1)
        rootPath = '/home/data1/Yiganduotou-Person/updateAll_scenes-20180702'
        path1 = 'HY1_1000'
#        draw_hist(os.path.join(rootPath,path1))
        path1 = 'HY1_1100'
 #       draw_hist(os.path.join(rootPath,path1))
        path1 = 'HY1_1400'
  #      draw_hist(os.path.join(rootPath,path1))
        path1 = 'HY1_1500'
   #     draw_hist(os.path.join(rootPath,path1))
        path1 = 'HY1_2000'
    #    draw_hist(os.path.join(rootPath,path1))
        path1 = 'HY1_3000'
     #   draw_hist(os.path.join(rootPath,path1))
        path1 = 'HY1_3001'
      #  draw_hist(os.path.join(rootPath,path1))
        path1 = 'HY1_4000'
       # draw_hist(os.path.join(rootPath,path1))
        path1 = 'HY1_5000'
#        draw_hist(os.path.join(rootPath,path1))
        path1 = 'HY1_6000'
#        draw_hist(os.path.join(rootPath,path1))
        path1 = 'HY1_7000'
#        draw_hist(os.path.join(rootPath,path1))
        path1 = 'HY1_8000'
#        draw_hist(os.path.join(rootPath,path1))
        path1 = 'HY1_9000'
        draw_hist(os.path.join(rootPath,path1))


	rootPath = '/home/lixiaoli/evaluate/data'
	path1 = os.path.join(rootPath,'HY1_2000_occlu20_cam5_1kID_delSideCam_F_K1','gallery')
	draw_hist(path1)
	path1 = os.path.join(rootPath,'HY1_2000_occlu20_cam5_1kID_delSideCam_F_K1','query')
	draw_hist(path1)
	path1 = os.path.join(rootPath,'HY1_3000_occlu20_cam5_delSideCam_F_K1','gallery')
        draw_hist(path1)
        path1 = os.path.join(rootPath,'HY1_3000_occlu20_cam5_delSideCam_F_K1','query')
        draw_hist(path1)
	path1 = os.path.join(rootPath,'HY1_4000_occlu20_cam5_1kID_delSideCam_F_K1','gallery')
        draw_hist(path1)
        path1 = os.path.join(rootPath,'HY1_4000_occlu20_cam5_1kID_delSideCam_F_K1','query')
        draw_hist(path1)
	path1 = os.path.join(rootPath,'HY1_5000_occlu20_cam5_1kID_delSideCam_F_K1','gallery')
        draw_hist(path1)
        path1 = os.path.join(rootPath,'HY1_5000_occlu20_cam5_1kID_delSideCam_F_K1','query')
        draw_hist(path1)
	path1 = os.path.join(rootPath,'HY1_6000_occlu20_cam5_1kID_delSideCam_F_K1','gallery')
        draw_hist(path1)
        path1 = os.path.join(rootPath,'HY1_6000_occlu20_cam5_1kID_delSideCam_F_K1','query')
        draw_hist(path1)
	path1 = os.path.join(rootPath,'HY1_7000_occlu20_cam5_1kID_delSideCam_F_K1','gallery')
        draw_hist(path1)
        path1 = os.path.join(rootPath,'HY1_7000_occlu20_cam5_1kID_delSideCam_F_K1','query')
        draw_hist(path1)
	path1 = os.path.join(rootPath,'HY1_all_occlu20_cam5_1kID_delSideCam_F_K1','gallery')
        draw_hist(path1)
        path1 = os.path.join(rootPath,'HY1_all_occlu20_cam5_1kID_delSideCam_F_K1','query')
        draw_hist(path1)
	
        path1 = '/home/data1/Yiganduotou-Person/updateAll-20180626'
        draw_hist(path1)
        rootPath = '/home/data1/Yiganduotou-Person/updateAll_scenes-20180626'
        path1 = os.path.join(rootPath,'HY1_1000')
        draw_hist(path1)
        path1 = os.path.join(rootPath,'HY1_1100')
        draw_hist(path1)
        path1 = os.path.join(rootPath,'HY1_2000')
        draw_hist(path1)
        path1 = os.path.join(rootPath,'HY1_3000')
        draw_hist(path1)
        path1 = os.path.join(rootPath,'HY1_3001')
        draw_hist(path1)
        path1 = os.path.join(rootPath,'HY1_4000')
        draw_hist(path1)
        path1 = os.path.join(rootPath,'HY1_5000')
        draw_hist(path1)
        path1 = os.path.join(rootPath,'HY1_6000')
        draw_hist(path1)
        path1 = os.path.join(rootPath,'HY1_7000')
        draw_hist(path1)
        path1 = os.path.join(rootPath,'HY1_8000')
        draw_hist(path1)
        path1 = os.path.join(rootPath,'HY1_9000')
	draw_hist(path1)
'''
'''
	path1 = '/home/lixiaoli/evaluate/data/HY1_2000_occlu20'
	draw_hist(path1)
	path1 = '/home/lixiaoli/evaluate/data/HY1_3000_occlu20'
        draw_hist(path1)
	path1 = '/home/lixiaoli/evaluate/data/HY1_4000_occlu20'
        draw_hist(path1)
	path1 = '/home/lixiaoli/evaluate/data/HY1_5000_occlu20'
        draw_hist(path1)
	path1 = '/home/lixiaoli/evaluate/data/HY1_6000_occlu20'
        draw_hist(path1)
	path1 = '/home/lixiaoli/evaluate/data/HY1_7000_occlu20'
        draw_hist(path1)
	path1 = '/home/lixiaoli/evaluate/data/HY1_8000_occlu20'
        draw_hist(path1)
	path1 = '/home/lixiaoli/evaluate/data/HY1_All_occlu20'
        draw_hist(path1)
#path1 = os.path.join(rootPath,'select_plus_new','gallery')
#path2 = os.path.join(rootPath,'select_plus_new','query')
#draw_hist(path1)
#draw_hist(path2)
'''
	
