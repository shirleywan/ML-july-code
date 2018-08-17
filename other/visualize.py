
source $1/config.sh

echo $DATA_PLACE/$DATA_NAME

python visualize_multiprocess.py $DATA_PLACE/$DATA_NAME $1 $DATA_PLACE/$DATA_NAME $2


