source ./beginTrain.config
echo class name: $TRAIN_CLASS
echo id number: $ID_NUMBER
echo train path: $TRAIN_PATH
echo is val: $USE_VAL
echo sleep: $SLEEP_TIME
echo save name: $SAVE_NAME
echo gpu: $GPU_ID
echo pre model: $PRE_MODEL
echo height: $HEIGHT
echo width: $WIDTH
echo batch_size: $BATCH_SIZE
echo FC6_SIZE: $FC6_SIZE
echo FC7_SIZE: $FC7_SIZE
echo LMDB_NAME: $LMDB_NAME
read -p 'continue?'

sleep $SLEEP_TIME

ext=_train_lmdb
#lmdbValPath=./examples/huawei/$LMDB_VAL_NAME$ext
#echo lmdbValPath: $lmdbValPath
#if [ ! -x "$lmdbValPath" ]; then
#    ./examples/huawei/create_huawei_ped.sh $VAL_PATH $USE_VAL $LMDB_VAL_NAME $HEIGHT $WIDTH
#    ./examples/huawei/make_huawei_ped_mean.sh $LMDB_VAL_NAME
#fi

lmdbPath=./examples/huawei/$LMDB_NAME$ext
echo lmdbPath: $lmdbPath
if [ ! -x "$lmdbPath" ]; then
    ./examples/huawei/create_huawei_ped.sh $TRAIN_PATH $USE_VAL $LMDB_NAME $HEIGHT $WIDTH
#    ./examples/huawei/make_huawei_ped_mean.sh $LMDB_NAME
fi


#sed -e '17c \    source: "examples/huawei/'$LMDB_NAME'_train_lmdb"' \
#   -e '18c \    batch_size: '$BATCH_SIZE \
#   -e '212c \    num_output: '$FC6_SIZE  \
#   -e '252c \    num_output: '$FC7_SIZE  \
#   -e '292c \    num_output: '$ID_NUMBER  train_vggm_lrn_softmax.prototxt > train.prototxt
#
#sed -e '17c \snapshot_prefix: "VGGM_LRN_HWP_HWR_'$SAVE_NAME'"' solver_vggm_lrn_softmax.prototxt > solver.prototxt

sed -e '17c \    source: "examples/huawei/'$LMDB_NAME'_train_lmdb"' \
   -e '18c \    batch_size: '$BATCH_SIZE \
   -e '321c \    num_output: '$FC6_SIZE  \
   -e '378c \    num_output: '$FC7_SIZE  \
   -e '435c \    num_output: '$ID_NUMBER  train_vggm_bn_softmax_192_96.prototxt > train.prototxt

#sed -e '17c \    source: "examples/huawei/'$LMDB_NAME'_train_lmdb"' \
#   -e '18c \    batch_size: '$BATCH_SIZE \
#   -e '37c \    source: "examples/huawei/'$LMDB_NAME'_train_val_lmdb"' \
#   -e '38c \    batch_size: '$VAL_BATCH_SIZE \
#   -e '339c \    num_output: '$FC6_SIZE  \
#   -e '396c \    num_output: '$FC7_SIZE  \
#   -e '453c \    num_output: '$ID_NUMBER  train_val_vggm_bn_softmax.prototxt > train.prototxt


#sed -e '17c \    source: "examples/huawei/'$LMDB_NAME'_train_lmdb"' \
#   -e '18c \    batch_size: '$BATCH_SIZE \
#   -e '37c \    source: "examples/huawei/'$LMDB_NAME'_train_val_lmdb"' \
#   -e '38c \    batch_size: '$VAL_BATCH_SIZE \
#   -e '339c \    num_output: '$FC6_SIZE  \
#   -e '396c \    num_output: '$FC7_SIZE  \
#   -e '453c \    num_output: '$ID_NUMBER  vggm_train_ImageNet.prototxt > train.prototxt

sed -e '17c \snapshot_prefix: "VGGM_BN_'$SAVE_NAME'"' solver_vggm_bn_softmax.prototxt > solver.prototxt


echo "begin to train"

./build/tools/caffe train --solver=solver.prototxt -weights=$PRE_MODEL -gpu $GPU_ID
#./build/tools/caffe train --solver=solver.prototxt -gpu $GPU_ID

echo $SAVE_NAME "finished!!"

