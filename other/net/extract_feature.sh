#!/usr/bin/env sh
 mkdir models/ped_attributes_V_3.7/feature/iter_10000
 cp models/ped_attributes_V_3.7/data/test.txt models/ped_attributes_V_3.7/feature/iter_10000
./build/tools/extract_features_binary \
 models/ped_attributes_V_3.7/caffemodel/VGGM_cls_iter_10000.caffemodel \
 models/ped_attributes_V_3.7/test.prototxt \
 fc10 \
 models/ped_attributes_V_3.7/feature/iter_10000/VGGM_cls_feature.dat \
 39
 
 mkdir models/ped_attributes_V_3.7/feature/iter_15000
 cp models/ped_attributes_V_3.7/data/test.txt models/ped_attributes_V_3.7/feature/iter_15000
./build/tools/extract_features_binary \
 models/ped_attributes_V_3.7/caffemodel/VGGM_cls_iter_15000.caffemodel \
 models/ped_attributes_V_3.7/test.prototxt \
 fc10 \
 models/ped_attributes_V_3.7/feature/iter_15000/VGGM_cls_feature.dat \
 39

 mkdir models/ped_attributes_V_3.7/feature/iter_20000
 cp models/ped_attributes_V_3.7/data/test.txt models/ped_attributes_V_3.7/feature/iter_20000
 ./build/tools/extract_features_binary \
 models/ped_attributes_V_3.7/caffemodel/VGGM_cls_iter_20000.caffemodel \
 models/ped_attributes_V_3.7/test.prototxt \
 fc10 \
 models/ped_attributes_V_3.7/feature/iter_20000/VGGM_cls_feature.dat \
 39
 
 mkdir models/ped_attributes_V_3.7/feature/iter_25000
 cp models/ped_attributes_V_3.7/data/test.txt models/ped_attributes_V_3.7/feature/iter_25000
 ./build/tools/extract_features_binary \
 models/ped_attributes_V_3.7/caffemodel/VGGM_cls_iter_25000.caffemodel \
 models/ped_attributes_V_3.7/test.prototxt \
 fc10 \
 models/ped_attributes_V_3.7/feature/iter_25000/VGGM_cls_feature.dat \
 39
 
 
 mkdir models/ped_attributes_V_3.7/feature/iter_30000
 cp models/ped_attributes_V_3.7/data/test.txt models/ped_attributes_V_3.7/feature/iter_30000
./build/tools/extract_features_binary \
 models/ped_attributes_V_3.7/caffemodel/VGGM_cls_iter_30000.caffemodel \
 models/ped_attributes_V_3.7/test.prototxt \
 fc10 \
 models/ped_attributes_V_3.7/feature/iter_30000/VGGM_cls_feature.dat \
 39
 
 
 mkdir models/ped_attributes_V_3.7/feature/iter_35000
 cp models/ped_attributes_V_3.7/data/test.txt models/ped_attributes_V_3.7/feature/iter_35000
./build/tools/extract_features_binary \
 models/ped_attributes_V_3.7/caffemodel/VGGM_cls_iter_35000.caffemodel \
 models/ped_attributes_V_3.7/test.prototxt \
 fc10 \
 models/ped_attributes_V_3.7/feature/iter_35000/VGGM_cls_feature.dat \
 39
 
 mkdir models/ped_attributes_V_3.7/feature/iter_40000
 cp models/ped_attributes_V_3.7/data/test.txt models/ped_attributes_V_3.7/feature/iter_40000
 ./build/tools/extract_features_binary \
 models/ped_attributes_V_3.7/caffemodel/VGGM_cls_iter_40000.caffemodel \
 models/ped_attributes_V_3.7/test.prototxt \
 fc10 \
 models/ped_attributes_V_3.7/feature/iter_40000/VGGM_cls_feature.dat \
 39
 
 
 mkdir models/ped_attributes_V_3.7/feature/iter_45000
 cp models/ped_attributes_V_3.7/data/test.txt models/ped_attributes_V_3.7/feature/iter_45000
 ./build/tools/extract_features_binary \
 models/ped_attributes_V_3.7/caffemodel/VGGM_cls_iter_45000.caffemodel \
 models/ped_attributes_V_3.7/test.prototxt \
 fc10 \
 models/ped_attributes_V_3.7/feature/iter_45000/VGGM_cls_feature.dat \
 39
 
 mkdir models/ped_attributes_V_3.7/feature/iter_50000
 cp models/ped_attributes_V_3.7/data/test.txt models/ped_attributes_V_3.7/feature/iter_50000
 ./build/tools/extract_features_binary \
 models/ped_attributes_V_3.7/caffemodel/VGGM_cls_iter_50000.caffemodel \
 models/ped_attributes_V_3.7/test.prototxt \
 fc10 \
 models/ped_attributes_V_3.7/feature/iter_50000/VGGM_cls_feature.dat \
 39
 
 
