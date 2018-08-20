#coding=utf-8
from PIL import Image, ImageDraw, ImageFont
import sys, getopt
import numpy as np
import os
import re
import random
import  xml.dom.minidom
from skimage import measure,draw , morphology

def getKey( x ):
    return  -int(x[1][3])//10

def get_obj_cls():
    obj_cls = {"ped": 1, "car": 2, "riding": 3, "riding_p": 4, "bike": 5}
    return obj_cls
    
def resizeImage(image_cv, accept = 514):
    width = image_cv.shape[0]
    height = image_cv.shape[1]
    maxDim = max(width,height)
    if height>width:
        ratio = float(accept/(height + 0.001))
    else:
        ratio = float(accept/(width + 0.001))
    image_cv = Image.fromarray(np.uint8(image_cv))
    image_cv = image_cv.resize((int(width*ratio), int(height*ratio)),resample=Image.BILINEAR)
    image_cv = np.array(image_cv)
    return image_cv
    
def myresize(image, accept = 514):
    width = image.size[0]
    height = image.size[1]
    maxDim = max(width,height)
    if height>width:
        ratio = float((accept + 0.001)/(height + 0.001))
    else:
        ratio = float((accept + 0.001)/(width + 0.001))
    #print ratio, (int(height*ratio), int(width*ratio))
    image = image.resize((int(width*ratio), int(height*ratio)),resample=Image.BILINEAR)
    return image

def myresize2(image, accept = 320):
    width = image.size[0]
    height = image.size[1]
    #print width, height
    maxDim = max(width,height)
    if height>width:
        ratio = float((accept + 0.001)/(height + 0.001))
    else:
        ratio = float((accept + 0.001)/(width + 0.001))
    #print ratio, (int(width*ratio), int(height*ratio))
    image = image.resize((int(width*ratio), int(height*ratio)),resample=Image.BILINEAR)
    return image
    
def get_offset_box(im, o_x, o_y, o_w, o_h, offset, rnd_offset):
    width, height = im.size
    if offset == "True":
        if rnd_offset == "True":
            a = random.uniform(-0.1, 0.1)
            b = random.uniform(-0.1, 0.1)
            c = 0
            d = 0
            c = random.uniform(-0.02, 0.02)
            d = random.uniform(-0.01, 0.01)
        else:
            a = 0.05
            b = 0.05
            c = 0
            d = 0
    else:
            a = 0
            b = 0
            c = 0
            d = 0
    dw = int(a * o_w)
    dh = int(b * o_h)
    dx = int((c) * o_w)
    dy = int((d) * o_h)
    w = o_w + dw
    h = o_h + dh
    x = o_x + dx - dw // 2
    y = o_y + dy - dh // 2

    box = [x, y, x + w, y + h]
    box = [max(0, box[0]), max(0, box[1]), min(width, box[2]), min(height, box[3])]
    return box
    
def verify_box(box, W, H):
    return [max(1, box[0]), max(1, box[1]), min(W - 1, box[2]), min(H - 1, box[3])]

def pad_box(box, pad_w, pad_h):
    return [box[0] - pad_w, box[1] - pad_h, box[2] + pad_w, box[3] + pad_h]
    
def my_print(name, lst):
    print "-------", name, "-------"
    for obj in lst:
        print obj
    
def _get_voc_color_map(n=256):
    color_map = np.zeros((n, 3), dtype = 'int64')
    
    for i in xrange(n):
        r = b = g = 0
        cid = i
        for j in xrange(0, 8):
            r = np.bitwise_or(r, np.left_shift(np.unpackbits(np.array([cid], dtype=np.uint8))[-1], 7-j))
            g = np.bitwise_or(g, np.left_shift(np.unpackbits(np.array([cid], dtype=np.uint8))[-2], 7-j))
            b = np.bitwise_or(b, np.left_shift(np.unpackbits(np.array([cid], dtype=np.uint8))[-3], 7-j))
            cid = np.right_shift(cid, 3)

        color_map[i][0] = r 
        color_map[i][1] = g
        color_map[i][2] = b
    return color_map
    
def getpallete(num_cls):
        # this function is to get the colormap for visualizing the segmentation mask
        n = num_cls
        pallete = [0]*(n*3)
        for j in xrange(0,n):
                lab = j
                pallete[j*3+0] = 0
                pallete[j*3+1] = 0
                pallete[j*3+2] = 0
                i = 0
                while (lab > 0):
                        pallete[j*3+0] |= (((lab >> 0) & 1) << (7-i))
                        pallete[j*3+1] |= (((lab >> 1) & 1) << (7-i))
                        pallete[j*3+2] |= (((lab >> 2) & 1) << (7-i))
                        i = i + 1
                        lab >>= 3
        return pallete
    
def show_masks(im, im_obj, W, H):
    for j in range(W):
        for i in range(H):
            if im_obj.getpixel((j,i)) == (0,0,0):
                im_obj.putpixel((j,i),im.getpixel((j,i)))
    return im_obj
    
    
def ext_size(x, y, width, height):
    #print x, y, width,height
    df_human_width = 24
    df_human_height = 58
    df_ext_height = 3
    ext_height = float(height * df_ext_height) / float(df_human_height - 2 * df_ext_height) + 0.5
    ext_width = float(ext_height * df_human_width) / float(df_human_height) + 0.5
    height = max(height - 2 * ext_height, 0)
    width = max(width - 2 * ext_width, 0)
    x = max(float(x + ext_width), 0)
    y = max(float(y + ext_height), 0)
    box = [x, y, x + width, y + height]
    box = [int(b) for b in box]
    #print box, ext_width, ext_height, width, height
    return box
    
def get_iou(box1, box2):
    inter_box = [max(box1[0], box2[0]), max(box1[1], box2[1]), min(box1[2], box2[2]), min(box1[3], box2[3])]
    a = abs(inter_box[2] - inter_box[0]) * abs(inter_box[3] - inter_box[1])
    b = abs(box1[2] - box1[0]) * abs(box1[3] - box1[1])
    c = abs(box2[2] - box2[0]) * abs(box2[3] - box2[1])
    iou = a / (b + c - a + 0.00001)
    if inter_box[2] < inter_box[0] or inter_box[3] < inter_box[1]:
        iou = 0
    return iou
    
    
def bbox_object(dir ,pic_name, W, H):
    #[idx, box, 0, type_cls, sn]
    type_cls = get_obj_cls()
    cnt = [0, 0]
    names = []
    objects = []
    name = dir + pic_name.zfill(8) + ".xml"
    #print name
    if os.path.isfile(name):
        names.append(name)
    name = dir + pic_name.zfill(7) + ".xml"
    #print name
    if os.path.isfile(name):
        names.append(name)
    if len(names) == 0:
        print "no box xml", name
        return objects
    #print names
    
    idxs = [51, 61, 711, 712, 713] #行人 骑行人 电瓶车 自行车 三轮车
    #打开xml文档
    for name in names:
        dom = xml.dom.minidom.parse(name)
        #print "dom:", dom
        #得到文档元素对象
        root = dom.documentElement
        Obj_lst = root.getElementsByTagName('Object')
        idx = 0
        for obj in Obj_lst:
            Rect = obj.getElementsByTagName("Rect")[0]
            id = int(Rect.getAttribute("id"))
            #print id
            if id not in idxs:
                continue
            if id == idxs[0]:
                width = int(Rect.getAttribute("width"))
                height = int(Rect.getAttribute("height"))
                sn = int(Rect.getAttribute("sn"))
                if height >= 80 and sn == 0:
                    x = int(Rect.getAttribute("x"))
                    y = int(Rect.getAttribute("y"))
                    box = ext_size(x, y, width, height)
                    box = verify_box(box, W, H)
                    sn = int(Rect.getAttribute("sn"))
                    object = [idx, box, 0, type_cls["ped"], sn]
                    if box[3] - box[1] >= 80:
                        objects.append(object)
                        cnt[0] = cnt[0] + 1
                continue

            if id == idxs[2] or id == idxs[3] or id == idxs[4]:
                width = int(Rect.getAttribute("width"))
                height = int(Rect.getAttribute("height"))
                sn = int(Rect.getAttribute("sn"))
                boxs=[]
                if sn > 0:
                    x = int(Rect.getAttribute("x"))
                    y = int(Rect.getAttribute("y"))
                    sn = int(Rect.getAttribute("sn"))
                    cbox = ext_size(x, y, width, height)
                    cbox = verify_box(cbox, W, H)
                    boxs.append([idx, cbox, 0, type_cls["bike"], sn])
                    m = 1
                    for p in Obj_lst:
                        Rect = p.getElementsByTagName("Rect")[0]
                        pid = int(Rect.getAttribute("id"))
                        psn = int(Rect.getAttribute("sn"))
                        if pid == idxs[1] and  psn == sn:
                            pwidth = int(Rect.getAttribute("width"))
                            pheight = int(Rect.getAttribute("height"))
                            px = int(Rect.getAttribute("x"))
                            py = int(Rect.getAttribute("y"))
                            pbox = ext_size(px, py, pwidth, pheight)
                            pbox = verify_box(pbox, W, H)
                            boxs.append([idx, pbox, 0, type_cls["riding_p"], sn])
                            cbox = [min(cbox[0], pbox[0]), min(cbox[1], pbox[1]), max(cbox[2], pbox[2]), max(cbox[3], pbox[3])]
                            m = m + 1
                    if (cbox[3] - cbox[1]) >= 80 and m > 1:
                        for b in boxs:
                            objects.append(b)
                        objects.append([idx, cbox, 0, type_cls["riding"], sn])
                continue
            idx = idx + 1
    return objects
    
def get_detectbox(fileObj):
    ##[dt_box ,cls, gt_box] 1 行人 2 机动车 3 骑行整体 4 骑行人 5 骑行工具
    boxes = []
    n_obj = 0
    n_cnt = 0
    line = "begin"
    is_cnt = False
    while line:
        line = fileObj.readline()
        line = line[0:-1]
        length = len(line)
        if length <= 0:
            return "no new image", []
        #print "line ", line
        lines = line.split(" ")
        if line[length - 1] == "g":
            imfile = lines[0]
            is_cnt = True
            continue
        if is_cnt:
            n_obj = int(line)
            n_cnt = 0
            is_cnt = False
            continue
        if n_cnt < n_obj:
            lines = [(float(ll)) for ll in lines]
            box = lines[0:4]
            n_cnt = n_cnt + 1
            if int(lines[-1]) in [1, 5] and lines[4] >= 0.5 and int(lines[5]) != 2:
                box = [int(l) for l in box]
                boxes.append([box, int(lines[5]), [-1, -1, -1, -1]])
        if n_cnt == n_obj:
            n_cnt = 0
            return imfile, boxes
    
def detect2boxgt(dt_objs, gt_objs):
    ##dt_objs:[box ,type_cls, bbox] 
    ##gt_objs:[idx, box, 0, type_cls, sn], all cls type
    ##type_cls: 1 行人 2 机动车 3 骑行整体 4 骑行人 5 骑行工具
    gt_objs.sort(key = getKey)
    for gt_obj in gt_objs:
        max_iou = 0
        match_obj = -1
        gt_cls = gt_obj[3]
        gt_box = gt_obj[1]
        j = 0
        for dt_obj in dt_objs:
            dt_cls = dt_obj[1]
            dt_box = dt_obj[0]
            if dt_cls == gt_cls and dt_obj != [-1, -1, -1, -1]:
                iou = get_iou(dt_box, gt_box)
                if iou > max_iou:
                    max_iou = iou
                    match_obj = j
            j = j + 1
        if max_iou > 0.5:
            dt_objs[match_obj][2] = gt_box
    return
    
def detect2boxgt2(dt_objs, gt_objs):
    ##dt_objs:[box ,type_cls, bbox] 
    ##gt_objs:[idx, box, 0, type_cls, sn], all cls type
    ##type_cls: 1 行人 2 机动车 3 骑行整体 4 骑行人 5 骑行工具
    dt_objs.sort(key = getKey)
    
    for dt_obj in dt_objs:
        dt_cls = dt_obj[1]
        dt_box = dt_obj[0]
        
        max_iou = 0
        match_obj = -1
        j = 0
        for gt_obj in gt_objs:
            gt_cls = gt_obj[3]
            gt_box = gt_obj[1]
            if gt_obj[2] == 0 and dt_cls == gt_cls:
                iou = get_iou(dt_box, gt_box)
                if iou > max_iou:
                    max_iou = iou
                    match_obj = j
            j = j + 1
        if max_iou > 0.5:
            dt_box[2] = gt_boxes[match_obj][1]
    return
    
    
def get_segbox(mask, W,H):
    mask =np.array(mask)
    mask[:,0] = 0
    mask[:, W - 1] = 0
    mask[0,:] = 0
    mask[H - 1, :] = 0
    mask = mask > 0
    mask = morphology.remove_small_objects(mask,min_size=50,connectivity=1)
    props = measure.regionprops(mask)
    seg_box = [9999, 9999, 0, 0]
    for prop in props:
        seg_box = [min(seg_box[1], prop.bbox[1]), min(seg_box[0], prop.bbox[0]), max(seg_box[3], prop.bbox[3]), max(seg_box[2], prop.bbox[2])]
    if len(props) == 0:
        seg_box = [0, 0, 1, 1]
    return seg_box
