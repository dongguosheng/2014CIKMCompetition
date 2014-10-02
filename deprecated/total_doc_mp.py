#! /usr/bin/python

import sys

def read_input(file):
	'''
		read input tf mapper-reducer file
		class:Queries\tword_1:val_1,word_2:val_2,.....
	'''
	for line in file:
		yield line

def main(separator='\t'):
	data = read_input(sys.stdin)
	for doc_line in data:
		print '%s%s%d' % ('Total count',separator,1)

if __name__ == '__main__':
	main()

