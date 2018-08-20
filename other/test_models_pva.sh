import os.path as osp
import sys
sys.path.append('/home/peiwenfang/caffe-master-pwf/python')

import numpy as np
from PIL import Image
import cv2
import caffe

import os
import argparse
from tools import SimpleTransformer
from skimage import measure,draw , morphology
from image_tool import resizeImage, myresize, myresize2, get_offset_box, verify_box, pad_box, my_print, _get_voc_color_map, getpallete, show_masks
    
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
        seg_box = [min(seg_box[1], prop.bbox[1]), min(seg_box[0], prop.bbox[0]), max(seg_box[3], prop.bbox[3]), max(seg_box[2], prop.bbox[2]), ]
    return seg_box
    
def tic():
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()

def toc(save_time, batchsize):
    import time
    if 'startTime_for_tictoc' in globals():
        fileObj = open(save_time,'a+')
        fileObj.write(str((time.time() - startTime_for_tictoc) * 1000 / batchsize) + "\n")
        fileObj.close()
        #print "Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds."
    else:
        print "Toc: start time not set"
    
def load_model(deploy_file, model_file):
    net = caffe.Net(deploy_file, model_file, caffe.TEST)
    return net
    
def segmenter(argv):
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', required=True, help='path to image')
    parser.add_argument('--mask_dir', required=True, help='path to mask')
    parser.add_argument('--show_dir', required=True, help='path to show_mask')
    parser.add_argument('--filelst', required=True, help='filelst to eval')
    parser.add_argument('--deploy_file' ,required=True, help='deploy_file')
    parser.add_argument('--model_file', required=True, help='caffe model_file')
    parser.add_argument('--gpudevice', type=int, default=0, help='gpudevice')
    parser.add_argument('--accept', type=int, default=320, help='accept size')
    parser.add_argument('--batchsize', type=int, default=20, help='batchsize')
    parser.add_argument('--offset', required=True, help='if offset')
    parser.add_argument('--pad', required=True, help='if pad')
    
    args = parser.parse_args()
    
    image_dir = args.image_dir
    showmask_dir = args.show_dir
    mask_dir = args.mask_dir
    image_list = args.filelst
    deploy_file = args.deploy_file
    model_file = args.model_file
    gpudevice = args.gpudevice
    accept = args.accept
    batchsize = args.batchsize
    offset = args.offset
    pad = args.pad
    
    #print argvs
    print "image_dir = {}".format(image_dir)
    print "showmask_dir = {}".format(showmask_dir)
    print "mask_dir = {}".format(mask_dir)
    print "image_list = {}".format(image_list)
    print "deploy_file = {}".format(deploy_file)
    print "model_file = {}".format(model_file)
    print "gpu_device = {}".format(gpudevice)
    print "accept = {}".format(accept)
    print "batchsize = {}".format(batchsize)
    print "offset = {}".format(offset)
    print "pad = {}".format(pad)
    
    save_time = deploy_file[0:deploy_file.rfind("/") + 1] + "test_time_" + str(batchsize) + ".txt"
    m_mean = [104.00699, 116.66877, 122.67892]
    transf = SimpleTransformer(m_mean)
    mean_vec = np.array([104.00699, 116.66877, 122.67892], dtype=np.float32)
    reshaped_mean_vec = mean_vec.reshape(1, 1, 3)
    if gpudevice >= 0:
        #Do you have GPU device? NO GPU is -1!
        has_gpu = 1
        #which gpu device is available?
        gpu_device=gpudevice#assume the first gpu device is available, e.g. Titan X
    else:
        has_gpu = 0
    if has_gpu==1:
        caffe.set_device(gpu_device)
        caffe.set_mode_gpu()
    else:
        caffe.set_mode_cpu()
    
    net = load_model(deploy_file, model_file)
    

    
    fileObj = open(image_list,'r')
    my_names = []
    offset_boxes = []
    seg_boxes =[]
    line = fileObj.readline()
    while line:
        line = line[0:-1]
        lines = line.split("; ")
        #print lines
        lines[0] = lines[0][0:-4]
        my_names.append(lines[0])
        #print line[1]
        if len(lines) > 1:
            seg_boxes.append(eval(lines[1]))
            offset_boxes.append(eval(lines[2]))
        line = fileObj.readline()
    fileObj.close()
    n_image = len(my_names)
    index = 0
    n_test = n_image // batchsize + 1
    for i in range(n_test):
        if i % 5 == 0:
            print i * batchsize, "---",n_image
        #if (i > 100):
        #    break
        files = []
        orgshapes = []
        cur_sizes = []
        crop_boxes = []
        n_patch = 0
        for itt in range(batchsize):
            
            if index >= n_image:
                break
	    if os.path.exists(image_dir + my_names[index] + ".jpg"):
		inputfile = image_dir + my_names[index] + ".jpg"
		im = Image.open(inputfile)
	    else:
		if os.path.exists(image_dir + my_names[index] + ".png"):
		    inputfile = image_dir + my_names[index] + ".png"
		    im = Image.open(inputfile)
                else:
		    continue
            #labelfile = "/home/geyunying/data/Object_Instance_1210/Segmentation2ClassAug/" + my_names[index] + ".png"
            #label = Image.open(labelfile)
            W, H = im.size
            crop_box = [0, 0, W, H]
            #offset_box = offset_boxes[index]
            #seg_box = seg_boxes[index]
            #crop_box = offset_box
            #if offset == "True":
            #    im_ifo = my_names[index].split("_")
            #    len_inf = len(im_ifo)
            #    x = int(im_ifo[len_inf - 5])
            #    y = int(im_ifo[len_inf - 4])
            #    w = int(im_ifo[len_inf - 3])
            #    h = int(im_ifo[len_inf - 2])
            #    offset_box = [x, y, x + w, y + h]
            #    crop_box = offset_box
            if pad == "True":
                offset_w = offset_box[2] - offset_box[0]
                offset_h = offset_box[3] - offset_box[1]
                pad_w = int(offset_h * 0.1)
                pad_h = pad_w
                crop_box = pad_box(offset_box, pad_w, pad_h)
                crop_box = verify_box(crop_box, W, H)
            crop_boxes.append(crop_box)
            im = im.crop(crop_box)
            org_shape = im.size
            maxDim = max(org_shape)
            im = myresize(im, accept)
            im = np.array(im, dtype=np.float32)
            im = im[:,:,::-1]
            im = im - reshaped_mean_vec
            
            cur_h, cur_w, cur_c = im.shape
            pad_h = accept - cur_h
            pad_w = accept - cur_w
            im = np.pad(im, pad_width=((0, pad_h), (0, pad_w), (0, 0)), mode = 'constant', constant_values = 0)
            
            im = im.transpose((2,0,1))
            #im = transf.preprocess(im)
            net.blobs['data'].data[itt, ...] = im
            orgshapes.append(org_shape)
            files.append(my_names[index])
            cur_sizes.append([cur_h, cur_w])
            index = index + 1
            n_patch = itt + 1
        tic()
        net.forward()
        toc(save_time, batchsize)
        
        prediction = net.blobs['segment_pred'].data
        #print n_patch
        for itt in range(n_patch):
            out = prediction[itt, ...].argmax(axis=0).astype(np.uint8)
            cur_size = cur_sizes[itt]
            cur_h = cur_size[0]
            cur_w = cur_size[1]
            out = out[0:cur_h, 0:cur_w]
            
            output_im = Image.fromarray(out)
            #output_im1 = Image.fromarray(out1)
            
            orgshape = orgshapes[itt]
            if output_im.size !=  orgshape:
                output_im = output_im.resize(orgshape, resample=Image.BILINEAR)
                #output_im1 = output_im1.resize(orgshape)
            maskfile = mask_dir + files[itt] + ".png"
            #print maskfile
            output_im.save(maskfile)
            #output_im1.save(crffile)
            
#            pallete = getpallete(256)
#            output_im.putpalette(pallete)
#            inputfile = image_dir + files[itt] + ".jpg"
#            input_image = Image.open(inputfile)
#            crop_box = crop_boxes[itt]
#            input_image = input_image.crop(crop_box)
#            W, H = input_image.size
#            output_im = show_masks(input_image, output_im, W, H)
#            input_image = input_image.convert('RGBA')
#            output_im = output_im.convert('RGBA')
#            superimpose_image = Image.blend(input_image, output_im, 0.6)
#            outputfile = showmask_dir + files[itt] + ".png"
#            superimpose_image.save(outputfile)
            
            


if __name__ == '__main__':
    segmenter(sys.argv[1:])

