#!/usr/bin/env python

import os

CLASS_DICT = {'VIDEO' : '1', 'NOVEL' : '2', 'GAME' : '3', 'TRAVEL' : '4', 'LOTTERY' : '5', 'ZIPCODE' : '6', 'OTHER' : '7', 'TEST' : '8'}
F_TRAIN = open('train_set.txt', 'w')
F_TEST_FEATURE = open('test_set.txt', 'w')
F_TEST_QUERY = open('test_queries.txt', 'w')


def gen_file_list(dir, file_num=73):
    '''
    Get the file list in the directory.
    '''
    for i in range(file_num):
        if i < 10:
            yield dir + '/part-0000' + str(i)
        else:
            yield dir + '/part-000' + str(i)

def read_file(filename):
    '''
    Read a file and append to train or test.
    '''
    with open(filename) as f:
        for line in f:
            class_list = []
            items = line.rstrip().split('\t')
            if len(items) < 2:
                print items
            else:
                for c, index in CLASS_DICT.items():
                    if c in items[0]:
                        class_list.append(index)
                if '8' in class_list:
                    F_TEST_QUERY.write(items[0] + '\n')
                    F_TEST_FEATURE.write(items[1] + '\n')
                else:
                    F_TRAIN.write('|'.join(class_list) + ' ' + items[1] + '\n')

def main():
    files = gen_file_list('./Data/tfidf_bigram', 73)
    for f in files:
        print f
        read_file(f)

    F_TRAIN.close()
    F_TEST_FEATURE.close()
    F_TEST_QUERY.close()

if __name__ == '__main__':
    main()