
# Path env
CAFFE_PATH=/home/chenxueqi/caffe-models/VGGM-evaModel
EVA_PLACE=/home/chenxueqi/caffe-models/evaluate
TEST_PLACE=$1

# Caffemodel
CAFFE_MODEL=`ls $TEST_PLACE|grep 'caffemodel\>'`
PROTOTXT_FILE=`ls $TEST_PLACE|grep 'prototxt\>'`
EXTRA_PROTO=$TEST_PLACE/extra.proto
GALLERY_PROTO=$TEST_PLACE/gallery.proto
QUERY_PROTO=$TEST_PLACE/query.proto

# Feature
FEATURE_PLACE=/home/chenxueqi/caffe-models/feature
OUT_LAYER=fc7
FEATURE_DIM=512
isHash=0
isNorm=1
isSig=0
## Distance alternative:
##  L1 , L2 , cos , Hamming
DISTANCE=cos

# Datas

## extra data
EXTRA_PLACE=/home/chenxueqi/caffe-models/data/bigDatas
### Name alternative: 
###  0 , Person_1320w , Person_120
EXTRA_NAME=0
EXTRA_LIST=$EXTRA_PLACE/${EXTRA_NAME}.list
EXTRA_PATH=$EXTRA_PLACE/${EXTRA_NAME}_path.list
if [ $EXTRA_NAME == 0 ];then
	EXTRA_FEAT=$FEATURE_PLACE/extra/0.feature
else
	EXTRA_FEAT=$FEATURE_PLACE/extra/${EXTRA_NAME}_${CAFFE_MODEL%.*}_${OUT_LAYER}.feature
	EXTRA_FEAT=$FEATURE_PLACE/extra/Person_1546w_vggm_bn_cam3_HWPtrain10_HYactor+Kako_Pre_iter_260000.feature
        
fi
EXTRA_COUNT=`cat $EXTRA_LIST|wc -l`

## data
DATA_PLACE=/home/chenxueqi/caffe-models/data
### Name alternative:
###  DB , 300ID-new , select , Big,select_plus,HWP_test,cyctist_sel,HYactor[1-4]
DATA_NAME=whole_query
DATA_FEAT_PLACE=$FEATURE_PLACE/$DATA_NAME
### gallery data
GALLERY_LIST=$DATA_PLACE/$DATA_NAME/gallery.list
GALLERY_PATH=$DATA_PLACE/$DATA_NAME/gallery_path.list
GALLERY_FEAT=$DATA_FEAT_PLACE/gallery_${CAFFE_MODEL%.*}_${OUT_LAYER}.feature
GALLERY_COUNT=`cat $GALLERY_LIST|wc -l`
### query data
QUERY_LIST=$DATA_PLACE/$DATA_NAME/query.list
QUERY_PATH=$DATA_PLACE/$DATA_NAME/query_path.list
QUERY_FEAT=$DATA_FEAT_PLACE/query_${CAFFE_MODEL%.*}_${OUT_LAYER}.feature
QUERY_COUNT=`cat $QUERY_LIST|wc -l`


# Save result file
PROCESS_MAX=100 #the top limit of amount of multiprocess, actually it depends on cpu count.
TOPN1=1000 # require: >100
TOPN2=10000 # require: >100 and >TOPN1
SAVE_NAME='result_'$CAFFE_MODEL'_'$DATA_NAME'_bn'
