#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def gen_train_files(input_file):
    '''
    Gen train file for s 4.
    '''
    output_file = '../Data/train_files/train_s4'
    
    with open(output_file, 'w') as f_out:
        with open(input_file) as f:
            for line in f:
                labels, feature = line.split('\t', 1)
                for i in range(7):
                    if str(i + 1) in labels:
                        f_out.write(str(i + 1) + ' ' + feature)

def main():
    if len(sys.argv) != 2:
        print 'Usage: ./gen_train_file_s4.py ../Data/train_feature'
    else:
        gen_train_files(sys.argv[1])

if __name__ == '__main__':
    main()