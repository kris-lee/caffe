# code for distinguishing and get train_txt and val_txt through the src_path
# auth : Li zhichao
# data : 2016-11-4


# -*- coding:utf-8 -*-
import os
import sys
import random

def get_file_list(src_path):
	total_file_list = []
	val_file_list = []
	for parent,dirnames,filenames in os.walk(src_path):
		if filenames:
			child = parent[parent.rfind('/')+1:]
			for filename in filenames:
				abspath = os.path.join(child,filename)
				total_file_list.append(abspath)


	# train_number : test_number = 9 : 1
	i = random.randint(0,9)
	while (i < len(total_file_list)):
		val_file_list.append(total_file_list[i])
		total_file_list = total_file_list[:i] + total_file_list[i+1:]
		i = i + 9


	# classify total into diffierent kind and save them to the train_txt
	with open(train_txt,'wb') as tt:
		for single_path in total_file_list:
			train_number = int(single_path[single_path.find('_')+1:single_path.rfind('.')])
			print 'train_number: ',train_number
			line = '%s %d\n' % (single_path,(train_number-1)/80)
			tt.write(line)		


	# classify total into diffierent kind and save them to the val_txt
	with open(val_txt,'wb') as tp:
		for single_path in val_file_list:
			val_number = int(single_path[single_path.find('_')+1:single_path.rfind('.')])
			print 'val_number: ',val_number
			line = '%s %d\n' % (single_path,(val_number-1)/80)
			tp.write(line)		

		

if __name__ == '__main__':
	src_path = '/training/images/'
	train_txt = '/training/label/train_list.txt'
	val_txt = '/training/label/val_list.txt'
	get_file_list(src_path)

