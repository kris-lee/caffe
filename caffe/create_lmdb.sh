# code for creating the data form of caffe(.lmdb) for training and testing(train_lmdb and test_lmdb)
# auth : Li zhichao
# data : 2016-11-2

#!/usr/bin/env sh
# Create the imagenet lmdb inputs
# N.B. set the path to the imagenet train + val data dirs


LMDB_ROOT=/training/lmdb
IMG_LIST_ROOT=/training/label/
TOOL_ROOT=/caffe09/build/tools


TRAIN_DATA_ROOT=/images/
VAL_DATA_ROOT=/images/


IMG_SIZE=256

# Set RESIZE=true to resize the images to 256x256. Leave as false if images have
# already been resized using another tool.
RESIZE=true

if $RESIZE; then
  RESIZE_HEIGHT=${IMG_SIZE}
  RESIZE_WIDTH=${IMG_SIZE}
else
  RESIZE_HEIGHT=0
  RESIZE_WIDTH=0
fi


if [ ! -d "$TRAIN_DATA_ROOT" ]; then
  echo "Error: TRAIN_DATA_ROOT is not a path to a directory: $TRAIN_DATA_ROOT"
  echo "Set the TRAIN_DATA_ROOT variable in create_imagenet.sh to the path" \
       "where the ImageNet validation data is stored."
  exit 1
fi

if [ ! -d "$VAL_DATA_ROOT" ]; then
  echo "Error: VAL_DATA_ROOT is not a path to a directory: $VAL_DATA_ROOT"
  echo "Set the VAL_DATA_ROOT variable in create_imagenet.sh to the path" \
       "where the ImageNet validation data is stored."
   exit 1
fi

echo "Creating train lmdb..."

GLOG_logtostderr=1 $TOOL_ROOT/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    -shuffle \
    $TRAIN_DATA_ROOT \
    $IMG_LIST_ROOT/train_list.txt \
    $LMDB_ROOT/train_lmdb


echo "Creating val lmdb..."

GLOG_logtostderr=1 $TOOL_ROOT/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    -shuffle \
    $VAL_DATA_ROOT \
    $IMG_LIST_ROOT/val_list.txt \
    $LMDB_ROOT/val_lmdb


echo "Done."
