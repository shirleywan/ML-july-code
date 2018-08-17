# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 14:13:13 2017

@author: p00355434
"""
# from __future__ import print_function
from PIL import Image as im

import xml.etree.cElementTree as et
import xml.dom.minidom as minidom
# import codecs
import os

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
##########################################################################################################################
### 生成标签
# savePath='D:\\HengYangLabelingData\\data\\FourkExportOut\\train\\'
# out_file=open('D:\\HengYangLabelingData\\data\\FourkExportOut\\label.txt','w')
# srcPath='D:\\Attribute-Data\\src\\FourkExportOut\\imgList.txt'
savePath = 'D:\\dataset\\save\\'
# out_file=open('D:\\dataset\\person-property\\1\\0734a007-1\\label.txt','w+')

srcPath = 'D:\\dataset\\person-property\\xian-3\\'
out_file = open(srcPath + '0_label.txt', 'w+')
dirs = os.listdir(srcPath)  # 仅返回一级目录
# dirs=open(srcPath,'r') #打开文件
count = 0
non_count = 0
total_kakou = 0
total_fkakou = 0
object_num = 0
for d in dirs:

    a = d[0:-1];
    if a.endswith(".jp"):
        # if a.endswith(".jp") :
        #     print('jpg exist')
        #
        # if (os.path.exists(srcPath+a.split('.jp')[0]+'.xml')):
        #     print('xml exist')

        if a.endswith(".jp") and os.path.exists(srcPath + a.split('.jp')[0] + '.xml'):  # xml  img 同时存在
            kakou_num = 0
            fkakou_num = 0
            xmlPath = srcPath + a.split('.jp')[0] + '.xml'
            try:
                # xml = et.parse(xmlPath).getroot()
                # print(type(xml))
                xml_tree = open(xmlPath, 'r').read()  # 返回XML形式的字符串
                xml = et.XML(xml_tree)
                # tree = ET.parse("country.xml")     #打开xml文档
                ## root = ET.fromstring(country_string) #从字符串传递xml
                # root = tree.getroot()     #获得root节点
                # print root[0][1].text    # 通过下标访问
                # print root[0].tag, root[0].text
            except:
                continue

            imgPath = srcPath + a.split('.jp')[0] + '.jpg'  # 第一个文件
            img = im.open(imgPath)

            print(imgPath)  # 输出文件路径
            # object_num=0
            for object in xml.iter('Object'):  # 遍历标注目标
                object_num += 1
                try:  # sn  type 是否存在
                    sn = object.attrib['sn']  # 个数
                    type = object.attrib['type']  # 类型
                except:
                    continue
                if type == 'non-motorized':
                    non_count += 1
                    print('non-motorized')
                    continue

                if type == 'Ped':  # 行人
                    count = count + 1
                    # 外接框  从frame中截取patch
                    fullPosition = object.find('Position')
                    # fullPosition = object.find('FullPosition')

                    if fullPosition is None:
                        continue
                    x, y, w, h = map(float, fullPosition.text.split(','))  # 赋值
                    if (h >= 500):
                        kakou_num = kakou_num + 1
                    if (h < 500):
                        fkakou_num = fkakou_num + 1
                        # if(h>=500):
                        #     x=int(x+0.5)
                        #     y=int(y+0.5)
                        #     w=int(w+0.5)#图片的宽
                        #     h=int(h+0.5)
                        #     if x<0 or y<0 or w<=0 or h<=0:
                        #         continue
                        #     ### padding 操作
                        #     padding=min(int(w*0.2),20)#需要w小于100，才会取到0.2W
                        #     x=x-padding
                        #     y=y-padding
                        #     w=w+2*padding
                        #     h=h+2*padding
                        #     if x<0:
                        #         x=0
                        #     if y<0:
                        #         y=0
                        #     if x+w>img.size[0]:
                        #         w=img.size[0]-x
                        #     if y+h>img.size[1]:
                        #         h=img.size[1]-y
                        #
                        #     print('    FullPosition = ' + str([x, y,  w,  h]))
                        #     tImg = img.crop((x, y, x + w, y + h)) #设置要裁剪的区域

                        #                             # 属性
                        #                             personProperty = object.find('PersonProperty')  # 是否存在
                        #                             if personProperty is None:
                        #                                continue
                        #
                        #                             res = [-1]*9
                        #                             label=0
                        #                             for p in personProperty:
                        #                                 # if p.tag == 'Sex':  #性别
                        #                                 #     if p.text == 'male':
                        #                                 #         res[0]=0
                        #                                 #         label=label+1
                        #                                 #         continue
                        #                                 #     if p.text == 'female':
                        #                                 #         res[0]=1
                        #                                 #         label = label + 1
                        #                                 #         continue
                        #
                        #                                 if p.tag == 'Age':  #年龄
                        #                                     if p.text == 'child':
                        #                                         res[1] = 0
                        #                                         label = label + 1
                        #                                         continue
                        #                                     if p.text=='youth':
                        #                                         res[1]=1
                        #                                         label=label+1
                        #                                         continue
                        #                                     if p.text == 'old':
                        #                                         res[1] = 2
                        #                                         label = label + 1
                        #                                         continue
                        #
                        # #                                if p.tag == 'View':#视角
                        # #                                    if p.text == 'frontal':
                        # #                                        res[4] = 1
                        # #                                        label = label + 4
                        # #                                    if p.text == 'back':
                        # #                                        res[5] = 1
                        # #                                        label = label + 4
                        # #                                    if p.text == 'leftprofiled':
                        # #                                        res[6] = 1
                        # #                                        label = label + 4
                        # #                                    if p.text == 'rightprofiled':
                        # #                                        res[7] = 1
                        # #                                        label = label + 4
                        #
                        #                                 # Crop: position with style, texture, color, secondcolor
                        #                                 if p.tag == 'Upper':
                        #                                         #style="t-shirt/sleeve/vest/naked"  4
                        #                                         #texture="plain/stripe/grid/logo/other" 5
                        #                                         #color="black/blue/brown/green/grey/orange/pink/purple/red/white/yellow" 6
                        #                                         #try:
                        #                                                ###判断是否有遮挡
                        #                                                if p.attrib['occlusion'] =='yes':
                        #                                                    continue
                        #                                                ###style
                        #                                                if p.attrib['style'] =='sleeve':
                        #                                                    res[2]=0
                        #                                                    label=label+1
                        #
                        #                                                if p.attrib['style'] =='t-shirt':
                        #                                                    res[2]=1
                        #                                                    label=label+1
                        #
                        #                                                if p.attrib['style'] =='vest':
                        #                                                    res[2]=2
                        #                                                    label=label+1
                        #
                        #                                                if p.attrib['style'] =='naked':
                        #                                                    res[2]=3
                        #                                                    label=label+1
                        #
                        #                                                 ###testure
                        #                                                if p.attrib['texture'] =='stripe' or p.attrib['texture'] =='hstripe'or p.attrib['texture'] =='vstripe':
                        #                                                    res[3]=0
                        #                                                    label=label+1
                        #
                        #                                                if p.attrib['texture'] =='grid' :
                        #                                                    res[3]=1
                        #                                                    label=label+1
                        #
                        #                                                if p.attrib['texture'] =='logo' :
                        #                                                    res[3]=2
                        #                                                    label=label+1
                        #
                        #                                                if p.attrib['texture'] =='other' :
                        #                                                    res[3]=3
                        #                                                    label=label+1
                        #
                        #                                                if p.attrib['texture'] =='plain' :
                        #                                                    res[3]=4
                        #                                                    label=label+1
                        #
                        #                                                ###color
                        #                                                if p.attrib['color'] =='black':
                        #                                                    res[4]=0
                        #                                                    label=label+1
                        #
                        #                                                if p.attrib['color'] =='green':
                        #                                                    res[4]=1
                        #                                                    label=label+1
                        #
                        #                                                if p.attrib['color'] =='white' :
                        #                                                    res[4]=2
                        #                                                    label=label+1
                        #
                        #                                                if p.attrib['color'] =='grey' :
                        #                                                    res[4]=3
                        #                                                    label=label+1
                        #                                                if p.attrib['color'] =='blue':
                        #                                                    res[4]=4
                        #                                                    label=label+1
                        #                                                if p.attrib['color'] =='yellow':
                        #                                                    res[4]=5
                        #                                                    label=label+1
                        #                                                if p.attrib['color'] =='orange' :
                        #                                                    res[4]=6
                        #                                                    label=label+1
                        #                                                if  p.attrib['color'] =='brown' :
                        #                                                    res[4]=7
                        #                                                    label=label+1
                        #                                                if p.attrib['color'] =='red'  :
                        #                                                    res[4]=8
                        #                                                    label=label+1
                        #                                                if  p.attrib['color'] =='pink'  :
                        #                                                    res[4]=9
                        #                                                    label=label+1
                        #                                                if  p.attrib['color'] =='purple' :
                        #                                                    res[4]=10
                        #                                                    label=label+1
                        #                                                # secondcolor
                        #                                                if p.attrib['secondcolor'] =='black':
                        #                                                    res[7]=0
                        #                                                    label=label+1
                        #                                                if p.attrib['secondcolor'] =='green':
                        #                                                    res[7]=1
                        #                                                    label=label+1
                        #                                                if p.attrib['secondcolor'] =='white' :
                        #                                                    res[7]=2
                        #                                                    label=label+1
                        #                                                if p.attrib['secondcolor'] =='grey' :
                        #                                                    res[7]=3
                        #                                                    label=label+1
                        #                                                if p.attrib['secondcolor'] =='blue':
                        #                                                    res[7]=4
                        #                                                    label=label+1
                        #                                                if p.attrib['secondcolor'] =='yellow':
                        #                                                    res[7]=5
                        #                                                    label=label+1
                        #                                                if p.attrib['secondcolor'] =='orange' :
                        #                                                    res[7]=6
                        #                                                    label=label+1
                        #                                                if  p.attrib['secondcolor'] =='brown' :
                        #                                                    res[7]=7
                        #                                                    label=label+1
                        #                                                if p.attrib['secondcolor'] =='red'  :
                        #                                                    res[7]=8
                        #                                                    label=label+1
                        #                                                if  p.attrib['secondcolor'] =='pink'  :
                        #                                                    res[7]=9
                        #                                                    label=label+1
                        #                                                if  p.attrib['secondcolor'] =='purple' :
                        #                                                    res[7]=10
                        #                                                    label=label+1
                        #
                        #
                        #                                         #except:
                        #                                         #    continue
                        #
                        #                                 # Crop: position with style, color, secondcolor
                        #                                 if p.tag == 'Lower':
                        #                                         #style="pants/trousers/skirt/dress"  4
                        #                                         #color="black/blue/brown/green/grey/orange/pink/purple/red/white/yellow" 6
                        #                                         #try:
                        #                                                 ###判断是否有遮挡
                        #                                                if p.attrib['occlusion'] =='yes':
                        #                                                    continue
                        #                                                ###style
                        #                                                if p.attrib['style'] =='trousers':
                        #                                                    res[5]=0
                        #                                                    label=label+1
                        #                                                if p.attrib['style'] =='pants':
                        #                                                    res[5]=1
                        #                                                    label=label+1
                        #                                                if p.attrib['style'] =='dress':
                        #                                                    res[5]=2
                        #                                                    label=label+1
                        #                                                if p.attrib['style'] =='skirt':
                        #                                                    res[5]=3
                        #                                                    label=label+1
                        #
                        #                                                 ###color
                        #                                                if p.attrib['color'] =='black':
                        #                                                    res[6]=0
                        #                                                    label=label+1
                        #                                                if p.attrib['color'] =='green':
                        #                                                    res[6]=1
                        #                                                    label=label+1
                        #                                                if p.attrib['color'] =='white' :
                        #                                                    res[6]=2
                        #                                                    label=label+1
                        #                                                if p.attrib['color'] =='grey' :
                        #                                                    res[6]=3
                        #                                                    label=label+1
                        #                                                if p.attrib['color'] =='blue':
                        #                                                    res[6]=4
                        #                                                    label=label+1
                        #                                                if p.attrib['color'] =='yellow':
                        #                                                    res[6]=5
                        #                                                    label=label+1
                        #                                                if p.attrib['color'] =='orange' :
                        #                                                    res[6]=6
                        #                                                    label=label+1
                        #                                                if  p.attrib['color'] =='brown' :
                        #                                                    res[6]=7
                        #                                                    label=label+1
                        #                                                if p.attrib['color'] =='red'  :
                        #                                                    res[6]=8
                        #                                                    label=label+1
                        #                                                if  p.attrib['color'] =='pink'  :
                        #                                                    res[6]=9
                        #                                                    label=label+1
                        #                                                if  p.attrib['color'] =='purple' :
                        #                                                    res[6]=10
                        #                                                    label=label+1
                        #                                                 # secondcolor
                        #                                                if p.attrib['secondcolor'] =='black':
                        #                                                    res[8]=0
                        #                                                    label=label+1
                        #                                                if p.attrib['secondcolor'] =='green':
                        #                                                    res[8]=1
                        #                                                    label=label+1
                        #                                                if p.attrib['secondcolor'] =='white' :
                        #                                                    res[8]=2
                        #                                                    label=label+1
                        #                                                if p.attrib['secondcolor'] =='grey' :
                        #                                                    res[8]=3
                        #                                                    label=label+1
                        #                                                if p.attrib['secondcolor'] =='blue':
                        #                                                    res[8]=4
                        #                                                    label=label+1
                        #                                                if p.attrib['secondcolor'] =='yellow':
                        #                                                    res[8]=5
                        #                                                    label=label+1
                        #                                                if p.attrib['secondcolor'] =='orange' :
                        #                                                    res[8]=6
                        #                                                    label=label+1
                        #                                                if  p.attrib['secondcolor'] =='brown' :
                        #                                                    res[8]=7
                        #                                                    label=label+1
                        #                                                if p.attrib['secondcolor'] =='red'  :
                        #                                                    res[8]=8
                        #                                                    label=label+1
                        #                                                if  p.attrib['secondcolor'] =='pink'  :
                        #                                                    res[8]=9
                        #                                                    label=label+1
                        #                                                if  p.attrib['secondcolor'] =='purple' :
                        #                                                    res[8]=10
                        #                                                    label=label+1
                        # #                                        except:
                        # #                                           continue
                        #
                        #
                        # #                                if label==7:
                        # #                                    break
                        #
                        # #                            if label==7:
                        #                             print('  Object sn = ' + sn + ', type = ' + type)
                        #                             #save img txt
                        #                             object_num=object_num+1
                        #                             tmpD=a.split('\\')
                        # del(tmpD[0:3])
                        #
                        # if tmpD[0]=='FourkExportOut':
                        #          del(tmpD[1])
                        # else:
                        #          del(tmpD[1:3])
                        # print(tmpD)
                        # mpD='_'.join(tmpD)
                        #   tmpD=tmpD[-1]

                        # imgName=tmpD.split('.jpg')[0]+'_'+str(object_num)+'.jpg'
                        # tImg.save(savePath+imgName)#存储在savepath路径下

                        # out_file.write(a.split('.jp')[0]+'.xml'+' ')#统计数据
                        # out_file.writelines('有%s 卡口，%s 泛卡口数据' % (kakou_num,fkakou_num))
                        # tmp=[str(i) for i in res]
                        # tmp=' '.join(tmp)
                        # out_file.write(tmp)
                        # print(imgName)
                        # print(tmp)
                        # out_file.write('\n')
        #out_file.write(a.split('.jp')[0] + '.xml' + ' ')  # 统计数据
        #out_file.writelines('有%s 卡口，%s 泛卡口数据' % (kakou_num, fkakou_num))
        #out_file.write('\n')

        total_kakou = total_kakou + kakou_num
        total_fkakou = total_fkakou + fkakou_num

out_file.write('\n')
out_file.writelines('文件夹图片中有 %s 个对象' % (object_num))
out_file.write('\n')
out_file.writelines('文件夹图片中有 %s 骑行' % (non_count))
out_file.write('\n')
out_file.writelines('文件夹图片中有 %s 行人 ' % (count))
out_file.write('\n')
out_file.writelines('有%s 卡口，%s 泛卡口数据' % (total_kakou, total_fkakou))
out_file.write('\n')
out_file.close()


##########################################################################################################################
