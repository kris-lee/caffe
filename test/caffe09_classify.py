#!/usr/bin/env python
"""
classify.py is an out-of-the-box image classifer callable from the command line.

By default it configures and runs the Caffe reference ImageNet model.
"""
import numpy as np
import os
import sys
import argparse
import glob
import time
import math
import cv2

import caffe


def get_imglist_from_file(listFile):
    strm = open(listFile)
    imglist = []
    for line in strm:
        if len(line) < 2:
            continue
        if line.endswith("\n"):
            imgUrl = line[:-1]
        else:
            imgUrl = line

        if imgUrl.find(" ") == -1:
            imglist.append(imgUrl)

    strm.close()

    return imglist


def main(argv):
    pycaffe_dir = os.path.dirname(__file__)

    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "input_file",
        help="Input image, directory, or npy."
    )
    parser.add_argument(
        "output_file",
        help="Result list file URL."
    )

    parser.add_argument(
        "--model_def",
        help="Model definition file."
    )
    parser.add_argument(
        "--pretrained_model",
        help="Trained model weights file."
    )
    parser.add_argument(
        "--gpu",
        action='store_true',
        help="Switch for gpu computation."
    )
    parser.add_argument(
        "--device_id",
        default = 0,
        type = int,
        help="gpu card id."
    )
    parser.add_argument(
        "--center_only",
        action='store_true',
        help="Switch for prediction from center crop alone instead of " +
             "averaging predictions across crops (default)."
    )
    parser.add_argument(
        "--not_crop",
        action='store_true'
    )
    parser.add_argument(
        "--image_dims",
        default='256,256',
        help="Canonical 'height,width' dimensions of input images."
    )
    parser.add_argument(
        "--mean_file",
        default="",
        help="Data set image mean of [Channels x Height x Width] dimensions " +
             "(numpy array). Set to '' for no mean subtraction."
    )
    parser.add_argument(
        "--input_scale",
        type=float,
        help="Multiply input features by this scale to finish preprocessing."
    )
    parser.add_argument(
        "--raw_scale",
        type=float,
        default=255.0,
        help="Multiply raw input by this scale before preprocessing."
    )
    parser.add_argument(
        "--channel_swap",
        default='2,1,0',
        help="Order to permute input channels. The default converts " +
             "RGB -> BGR since BGR is the Caffe default by way of OpenCV."
    )
    parser.add_argument(
        "--ext",
        default='jpg',
        help="Image file extension to take as input when a directory " +
             "is given as the input file."
    )
    args = parser.parse_args()

    image_dims = [int(s) for s in args.image_dims.split(',')]
    print "image_dims: ", image_dims

    mean, channel_swap = None, None
    if not args.mean_file == "":
        mean = np.load(args.mean_file)
        mean = mean.mean(1).mean(1)
        print "mean: ", mean
    else:
        mean = np.zeros(3)
    if args.channel_swap:
        channel_swap = [int(s) for s in args.channel_swap.split(',')]

    if args.gpu:
        caffe.set_mode_gpu()
        caffe.set_device(args.device_id)
        print("GPU mode")
    else:
        caffe.set_mode_cpu()
        print("CPU mode")

    # Make classifier.
    classifier = caffe.Classifier(args.model_def, args.pretrained_model,
            image_dims=image_dims, mean=mean,
            input_scale=args.input_scale, raw_scale=args.raw_scale,
            channel_swap=channel_swap)

    # Load all image list.
    args.input_file = os.path.expanduser(args.input_file)
    allImgs = get_imglist_from_file(args.input_file)

    # Open result file
    resStrm = open(args.output_file, "w")

    # Set batch size
    netInShape = classifier.blobs[classifier.inputs[0]].data.shape
    print "netInShape: ", netInShape
    dim0_proto = netInShape[0]
    if args.center_only or args.not_crop:
        batchSize = dim0_proto
    else:
        batchSize = dim0_proto / 10
    if batchSize < 1:
        batchSize = 1
    print "batchSize: ", batchSize

    # set size of resize to
    resizeWidth = image_dims[1]
    resizeHeight = image_dims[0]
    if args.not_crop:
        resizeWidth = netInShape[3]
        resizeHeight = netInShape[2]

    # Get one batch
    batch_num = int(math.ceil(float(len(allImgs)) / batchSize))
    print "batch_num: ", batch_num
    for batch in range(batch_num):
        if batch == batch_num - 1:
            imgNum_thisBatch = len(allImgs) - batch * batchSize
        else:
            imgNum_thisBatch = batchSize

        start = batch * batchSize
        inputs = []
        preImgs = []
        time1 = time.time()
        for i in range(imgNum_thisBatch):
            imgUrl = os.path.expanduser(allImgs[start+i])
            try:
                img = caffe.io.load_image(imgUrl)
                img = caffe.io.resize_image(img, (resizeHeight, resizeWidth, 3))
                inputs.append(img) 
            except:
                #print "Load image ", imgUrl, " failed and skipped!"
                continue
            
            preImgs.append(imgUrl)

        imgNum_thisBatch = len(preImgs)
        if imgNum_thisBatch < 1:
            continue

        time2 = time.time()
        #print "Load and resize time: ", time2-time1

        # Predict.
        start_time = time.time()
        #print "Predicting image: ", start, " to ", start+imgNum_thisBatch-1
        predictions = classifier.predict(inputs, not args.center_only, args.not_crop)
        end_time = time.time()
        #print "Resize and prediction time: ", end_time-start_time

        # Sort by score
        sortedScores = []
        sortedTags = []
        for i in range(predictions.shape[0]):
            scoreList = predictions[i].tolist()
            sortedScoreList = sorted(scoreList, reverse=True)

            sortedTagList = []
            for j in range(len(scoreList)):
                tag = scoreList.index(sortedScoreList[j])
                sortedTagList.append(tag)
            
            sortedScores.append(sortedScoreList)
            sortedTags.append(sortedTagList)

        # Save result
        #print sortedTags
        for i in range(imgNum_thisBatch):
            resStrm.write(preImgs[i])
            for j in range(len(sortedTags[i])):
                resStrm.write(" " + str(sortedTags[i][j]) + " " + str(sortedScores[i][j]))

            resStrm.write("\n")
    

if __name__ == '__main__':
    main(sys.argv)
    print "Done."
