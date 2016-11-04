# code for running caffe
# auth : Li zhichao
# data : 2016-11-2

#/usr/bin/env sh

# caffe model here apply GoogleNet


/caffe09/build/tools/caffe train \
    --solver=./solver.prototxt \
    --weights=/caffe09/models/bvlc_googlenet/bvlc_googlenet_ilsvrc2012.caffemodel \
	--gpu=0
