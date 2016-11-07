# code for get the score basic on the test_list.txt and store the result with the form of score_test_list.txt
# auth : Li zhichao
# data : 2016-11-7
# than : liuyuming who provides the tools
# tool : caffe09_classify.py , deploy.prototxt , places_mean.npy

# caffemodel is the trainning result stored in the snapshots
# devide_id is the number of GPU to run the code

#!/bin/bash


python /caffe09/python/caffe09_classify.py \
	./test_list.txt \
	./score_test_list.txt \
	--model_def ./deploy.prototxt \
	--pretrained_model /caffe09/models/bvlc_googlenet/snapshots/bvlc_googlenet_iter_40000.caffemodel \
	--mean_file ./places_mean.npy \
	--gpu \
	--device_id 0 \
	--not_crop 
