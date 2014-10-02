#!/usr/bin/env python

# -*- coding: utf-8 -*-

import sys
from operator import itemgetter

CLASS_LIST = ['VIDEO', 'NOVEL', 'GAME', 'TRAVEL', 'LOTTERY', 'ZIPCODE', 'OTHER']

def gen_final_result(test, result_file, query_dict):
    f_result = open(result_file, 'w')
    with open(test) as f:
        for line in f:
            if line.rstrip() in query_dict:
                f_result.write(line.rstrip() + '\t' + query_dict[line.rstrip()] + '\n')
            else:
                print line + 'Not Found, labeled to OTHER!!!'
                f_result.write(line.rstrip() + '\t' + 'CLASS=OTHER\n')

def gen_proba_list(test_query, result_file, threshold):
    query_dict = {}

    f_result = open(result_file)

    index_list = f_result.readline().rstrip().split()[1: ]

    with open(test_query) as f:
        for line in f:
            query = line.rstrip()
            proba_list = f_result.readline().rstrip().split()[1: ]
            for i in range(len(proba_list)):
                proba_list[i] = (proba_list[i], int(index_list[i]) - 1)

            proba_list = sorted(proba_list, key=itemgetter(0), reverse=True)
            if proba_list[1][0] > float(threshold):
                query_dict[query] = ' | '.join(['CLASS=' + CLASS_LIST[proba_c[1]] for proba_c in proba_list[: 2]])
            else:
                query_dict[query] = ' | '.join(['CLASS=' + CLASS_LIST[proba_c[1]] for proba_c in proba_list[: 1]])
    return query_dict

def main():
    if len(sys.argv) != 6:
        print 'Usage: ./gen_final_result_s4.py ../Data/test_query ./predict_results/ threshold ../Data/test.txt ./final_result'
    else:
        query_dict = gen_proba_list(sys.argv[1], sys.argv[2], sys.argv[3])
        gen_final_result(sys.argv[4], sys.argv[5], query_dict)

if __name__ == '__main__':
    main()