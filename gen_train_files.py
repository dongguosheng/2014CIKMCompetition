#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def gen_train_files(input_file):
    '''
    Gen 7 train files.
    '''
    output_file = '../Data/train_files/train_'
    file_list = []
    for i in range(7):
        file_list.append(open(output_file + str(i), 'w'))

    with open(input_file) as f:
        for line in f:
            labels, feature = line.split('\t', 1)
            for i in range(7):
                if str(i + 1) in labels:
                    file_list[i].write('1 ' + feature)
                else:
                    file_list[i].write('-1 ' + feature)

    for f in file_list:
        f.close()

def main():
    if len(sys.argv) != 2:
        print 'Usage: ./gen_train_files.py ../Data/train_feature'
    else:
        gen_train_files(sys.argv[1])

if __name__ == '__main__':
    main()