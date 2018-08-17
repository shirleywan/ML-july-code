path1 = $DATA_PLACE/$DATA_NAME

source $2/config.sh
path2=$DATA_PLACE/$DATA_NAME

python 2-visualize-compare.py $path1 $path2 $3 $1 $2
