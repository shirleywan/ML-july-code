if [ ! -n "$1" ];then
	echo 'Please input a data name!'
	exit 1
fi

if [ ! -d "$1" ];then
	echo $1' does not exist!'
	exit 1
fi


ls $1/gallery > $1/gallery.list
echo 'Generated: '$1'/gallery.list'
ls $1/query > $1/query.list
echo 'Generated: '$1'/query.list'
if [ -d "$1/train" ];then
	ls $1/train > $1/train.list
	echo 'Generated: '$1'/train.list'
fi

sed 's#^#/home/chenxueqi/caffe-models/data/'$1'/gallery/##' $1/gallery.list > $1/gallery_path.list
echo 'Generated: '$1'/gallery_path.list'
sed 's#^#/home/chenxueqi/caffe-models/data/'$1'/query/##' $1/query.list > $1/query_path.list
echo 'Generated: '$1'/query_path.list'
if [ -d "$1/train" ];then
	sed 's#^#/home/dingyuhang/data/'$1'/train/##' $1/train.list > $1/train_path.list
	echo 'Generated: '$1'/train_path.list'
fi

echo 'finished.'
