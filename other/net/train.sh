#!/bin/bash 
GLOG_logtostderr=0 GLOG_log_dir=models/ped_attributes_V_3.7/Log/ ./build/tools/caffe train --solver=models/ped_attributes_V_3.7/solver.prototxt --weights=/home/peiwenfang/caffe-master/VGG_CNN_M_1024.v2.caffemodel -gpu=0
