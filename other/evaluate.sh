#################################
# Initialize environment
if [ ! -n "$1" ];then
    echo 'Usage: ./'$0' [test path] [config path]'
    exit 1
fi

if [ ! -n "$2" ];then
    source $1/config.sh
else
    source $2
fi

echo -e '\e[01;32mExtraction Environment:\e[0m'
echo -e '\e[33m Caffe model >\t\e[0m '$CAFFE_MODEL
echo -e '\e[33mOutput layer >\t\e[0m '$OUT_LAYER
echo -e '\e[33m Feature dim >\t\e[0m '$FEATURE_DIM
echo -e '\e[33m  Extra data >\t\e[0m '$EXTRA_NAME' '$EXTRA_COUNT
echo -e '\e[33m        data >\t\e[0m '$DATA_NAME
echo -e '\e[33m     Gallery >\t\e[0m '$GALLERY_COUNT
echo -e '\e[33m       Query >\t\e[0m '$QUERY_COUNT

#################################
# Preprocess
#export PYTHONPATH=PYTHONPATH:vggm_bn/prototxt_custom:~/caffe-master/python
echo
echo 'Generating new prototxt...'
SHUFFLE=False

#sed -e '14c \    source: "'$EXTRA_PATH'"' $TEST_PLACE/$PROTOTXT_FILE > $EXTRA_PROTO
sed -e '14c \    source: "'$GALLERY_PATH'"' $TEST_PLACE/$PROTOTXT_FILE > $GALLERY_PROTO
sed -e '14c \    source: "'$QUERY_PATH'"' $TEST_PLACE/$PROTOTXT_FILE > $QUERY_PROTO

echo $EVA_PLACE/$WORK_PATH_CUSTOM
echo $CUSTOM_SOURCE_GALLERY
echo $CUSTOM_BATCHSIZE
echo $CUSTOM_SOURCE_QUERY
echo $GALLERY_LIST
echo $QUERY_LIST
mkdir -p $DATA_FEAT_PLACE
#################################
# # Extract feature
echo
FLIP=0
echo -e '\e[01;31m[ EXTRACTION ]\e[0m'
#echo 'Extracting Extra...'
#result1=`$CAFFE_PATH/build/tools/extract_features.bin $TEST_PLACE/$CAFFE_MODEL $EXTRA_PROTO $OUT_LAYER $EXTRA_FEAT $EXTRA_COUNT lmdb GPU`
echo 'Extracting Gallary...'
echo $TEST_PLACE/$CAFFE_MODEL
result2=`$CAFFE_PATH/build/tools/extract_features.bin $TEST_PLACE/$CAFFE_MODEL $GALLERY_PROTO $OUT_LAYER $GALLERY_FEAT $GALLERY_COUNT lmdb GPU 0`
echo $GALLERY_PROTO #$OUT_LAYER $GALLERY_FEAT $GALLERY_COUNT
echo 'Extracting Query...'
result3=`$CAFFE_PATH/build/tools/extract_features.bin $TEST_PLACE/$CAFFE_MODEL $QUERY_PROTO $OUT_LAYER $QUERY_FEAT $QUERY_COUNT lmdb GPU 0`

if [[ $FLIP -eq 1 ]];then
    echo 'Extracting Gallery...'
    echo $TEST_PLACE/$CAFFE_MODEL
    sed -e '11c \    mirror: True' $GALLERY_PROTO > $GALLERY_FLIP_PROTO
    result2_flip=`$CAFFE_PATH/build/tools/extract_features.bin $TEST_PLACE/$CAFFE_MODEL $GALLERY_FLIP_PROTO $OUT_LAYER $GALLERY_FLIP_FEAT $GALLERY_COUNT lmdb GPU`
    echo 'Extracting Query...'
    sed -e '11c \    mirror: True' $QUERY_PROTO > $QUERY_FLIP_PROTO
    result3_flip=`$CAFFE_PATH/build/tools/extract_features.bin $TEST_PLACE/$CAFFE_MODEL $QUERY_FLIP_PROTO $OUT_LAYER $QUERY_FLIP_FEAT $QUERY_COUNT lmdb GPU`
fi
#result3=`$CAFFE_PATH/build/tools/extract_features.bin $TEST_PLACE/$CAFFE_MODEL $QUERY_PROTO $OUT_LAYER market_test $QUERY_COUNT lmdb GPU`
#rm $EXTRA_PROTO
#rm $GALLERY_PROTO
#rm $QUERY_PROTO

#################################
# Query
echo
echo -e '\e[01;31m[ QUERY ]\e[0m'
$EVA_PLACE/query.sh $1
