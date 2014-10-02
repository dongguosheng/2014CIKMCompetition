#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def gen_labeled_data(input_file, labeled_file, unknown_file):
    '''
    Split input file to labeled file and unknown file.
    '''
    f_labeled = open(labeled_file, 'w')
    f_unknown = open(unknown_file, 'w')

    with open(input_file) as f:
        isLabeled = False
        for line in f:
            if 'UNKNOWN' in line:
                isLabeled = False
                f_unknown.write(line)
            elif 'VIDEO' in line or 'NOVEL' in line or 'GAME' in line or 'TRAVEL' in line or 'LOTTERY' in line or 'ZIPCODE' in line or 'OTHER' in line or 'TEST' in line or isLabeled:
                isLabeled = True
                f_labeled.write(line)
            elif isLabeled:
                f_unknown.write(line)
            elif not isLabeled:
                f_labeled.write(line)

    f_labeled.close()
    f_unknown.close()

def main():
    if(len(sys.argv) != 4):
        print 'Usage: ./gen_labeled_data.py initial_file labeled_file unknown_file'
    else:
        gen_labeled_data(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == '__main__':
    main()