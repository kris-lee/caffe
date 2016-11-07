# code for getting the url of iamge for testing the accuracy
# auth : Li zhichao
# data : 2016-11-7


import os


dstStrm = open("/test/uri_list.txt", "w")
imgRoot = "/images/image_test/"
allBackends = [".bmp", ".BMP", ".jpg", ".JPG", ".png", ".PNG"]

imgNum = 0
for root, dir, files in os.walk(imgRoot):
	for imgName in files:
		pos = imgName.rfind(".")
		backend = imgName[pos:]
		if not backend in allBackends:
			continue
		imgUrl = os.path.join(root, imgName)
		dstStrm.write(imgUrl+"\n")

		imgNum += 1

print "imgNum: ", imgNum

dstStrm.close()

