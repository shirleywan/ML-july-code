#!/usr/bin/env sh
# Compute the mean image from the imagenet training lmdb
# N.B. this is available in data/ilsvrc12

DATA=models/huawei_attributes_3
DIRPATH=models/huawei_attributes_3
TOOLS=build/tools

$TOOLS/compute_image_mean $DATA/attributes_train_lmdb_for_mean \
  $DIRPATH/attributes_mean_train.binaryproto

echo "Done."
