# code for getting the real classification basic on true data
# auth : Li zhichao
# data : 2016-11-7


# -*- coding:utf-8 -*-
import os
import sys
import random

def get_file_list(total_text):

	test_file_list = []
	lines = open(total_text).readlines()

	for j in range(0,len(lines)):
		test_file_list.append(lines[j][:-1])

	# supposing that we just devide things into two kinds
	dict = {'Type_A': 0, 'Type_B': 1}

	with open(test_txt,'wb') as tt:
		for single_path in test_file_list:
			abspath = single_path[:single_path.rfind('/')]
			category = abspath[abspath.rfind('/')+1:single_path.rfind('/')]
			line = '%s %d\n' % (single_path,dict[category])
			tt.write(line)		


		

if __name__ == '__main__':
	total_text = 'label/test/uri_list.txt'
	test_txt = 'label/true_classificiation_list.txt'
	get_file_list(total_text)

