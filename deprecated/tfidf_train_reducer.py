#!/usr/bin/env python

from itertools import groupby
from operator import itemgetter
import sys

def read_mapper_output(file, separator='\t'):
	for line in file:
		yield line.rstrip().split(separator, 1)


def main(separator='\t'):
	'''
		word count reducer
	'''
	data = read_mapper_output(sys.stdin, separator=separator)
	for current_word, group in groupby(data, itemgetter(0)):
		feature = ''
		for queries, value in group:
			feature = value
		
		temp_list = feature.split(' ', 1)
		if len(temp_list) < 2:
			pass
		else:
			for c in temp_list[0].split('|'):
				print c + ' ' + temp_list[1]

if __name__ == "__main__":
	main()
