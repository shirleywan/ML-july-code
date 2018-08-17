#################################
# Initialize environment
if [ ! -n "$1" ];then
    echo 'Usage: ./'$0' [test path] [config path]'
    exit 1
fi

if [ ! -n "$2" ];then
    source $1/config.sh
    echo 'helo'
else
    source $2
fi
echo -e '\e[01;32mQuery Environment:\e[0m'
echo -e '\e[33m Caffe model >\t\e[0m '$CAFFE_MODEL
echo -e '\e[33mOutput layer >\t\e[0m '$OUT_LAYER
echo -e '\e[33m Feature dim >\t\e[0m '$FEATURE_DIM
echo -e '\e[33m  Extra data >\t\e[0m '$EXTRA_NAME' '$EXTRA_COUNT
echo -e '\e[33m    Key data >\t\e[0m '$DATA_NAME
echo -e '\e[33m     Gallery >\t\e[0m '$GALLERY_COUNT
echo -e '\e[33m       Query >\t\e[0m '$QUERY_COUNT
echo -e '\e[33m   Normalize >\t\e[0m '$isNorm
echo -e '\e[33m     Sigmoid >\t\e[0m '$isSig
echo -e '\e[33m        Hash >\t\e[0m '$isHash
echo -e '\e[33m    Distance >\t\e[0m '$DISTANCE
echo -e '\e[33m TopN1,TopN2 >\t\e[0m '$TOPN1' '$TOPN2
echo -e '\e[33m Process max >\t\e[0m '$PROCESS_MAX
echo -e '\e[33m Result name >\t\e[0m '$SAVE_NAME

RANK_PATH=$TEST_PLACE/$SAVE_NAME/rankFiles

mkdir -p $RANK_PATH
mkdir -p $TEST_PLACE/archive

cp $1/config.sh $TEST_PLACE/$SAVE_NAME/config.sh

#################################
# Query
echo
echo -e '\e[01;31m[ QUERY ]\e[0m'
FLIP=0
if [[ $FLIP -eq 1 ]];then
    echo 'hello2'
    python $EVA_PLACE/query_new.py $EXTRA_FEAT $GALLERY_FEAT $QUERY_FEAT $EXTRA_LIST $GALLERY_LIST $QUERY_LIST $RANK_PATH $FEATURE_DIM $isNorm $isSig $isHash $DISTANCE $TOPN2 $PROCESS_MAX $EXTRA_FLIP_FEAT $GALLERY_FLIP_FEAT $QUERY_FLIP_FEAT
else
    echo 'hello1'
    python $EVA_PLACE/query_new.py $EXTRA_FEAT $GALLERY_FEAT $QUERY_FEAT $EXTRA_LIST $GALLERY_LIST $QUERY_LIST $RANK_PATH $FEATURE_DIM $isNorm $isSig $isHash $DISTANCE $TOPN2 $PROCESS_MAX
fi
echo -e '\e[31mQuery finished!\e[0m'
echo

#################################
# Statistic
echo
echo -e '\e[01;31m[ RANK ]\e[0m'
python $EVA_PLACE/rank_new.py $TEST_PLACE $SAVE_NAME $EXTRA_LIST $GALLERY_LIST $TOPN1 $TOPN2
echo -e '\e[031mRank finished!\e[0m'
echo
echo -e '\e[01;031m--- ALL FINISHED ---\e[0m'
echo "caffe model: $CAFFE_MODEL data name:  $DATA_NAME"> $TEST_PLACE/archive/$SAME_NAME/summary1.txt

