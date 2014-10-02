#! /usr/bin/python

import sys

def read_input(file):
	'''
		read input tf mapper-reducer file
		class:Queries\tword_1:val_1,word_2:val_2,.....
	'''
	for line in file:
		yield line.split('\t')

def str_to_dict(term_val_pairs):
	'''
		make the 'word:val,.....' str to dict
	'''
	term_val_dict = {}
	term_val_list = term_val_pairs.split(',')
	for term_val in term_val_list:
		term,val = term_val.split(':')
		try:
			if term in term_val_dict:
				term_val_dict[term] += int(val)
			else:
				term_val_dict[term] = int(val)
		except ValueError:
			pass
	return term_val_dict

def main(separator='\t'):
	data = read_input(sys.stdin)
	for qt_record in data:
		key,term_val_pairs = qt_record
		term_val_dict = str_to_dict(term_val_pairs.rstrip().split('+')[-1])
		for term in term_val_dict.keys():
			print '%s%s%d' % (term,separator,1)

if __name__ == '__main__':
	main()

