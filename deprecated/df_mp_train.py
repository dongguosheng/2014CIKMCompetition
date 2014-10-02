#! /usr/bin/python

import sys

def read_input(file):
	'''
		read input tf mapper-reducer file
		class:Queries\tword_1:val_1,word_2:val_2,.....
	'''
	for line in file:
		yield line.rstrip().split(' ', 1)

def str_to_list(term_val_pairs):
	'''
		make the 'word:val,.....' str to dict
	'''
	key_list = []
	term_val_list = term_val_pairs.split()
	for term_val in term_val_list:
		term,val = term_val.split(':')
		key_list.append(term)
	return key_list

def main(separator='\t'):
	data = read_input(sys.stdin)
	for qt_record in data:
		print qt_record
		key,term_val_pairs = qt_record
		key_list = str_to_list(term_val_pairs)
		for term in key_list:
			print '%s%s%d' % (term,separator,1)

if __name__ == '__main__':
	main()

