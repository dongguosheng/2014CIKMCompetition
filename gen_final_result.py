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

def gen_proba_list(test_query, result_dir, threshold):
    query_dict = {}
    if result_dir[-1] != '/':
        result_dir += '/'
    f_result_list = []
    for i in range(7):
        f_result_list.append(open(result_dir + 'result_' + str(i)))
    index_list = []
    for f in f_result_list:
        temp_list = f.readline().rstrip().split()
        index_list.append(temp_list.index('1'))

    with open(test_query) as f:
        for line in f:
            query = line.rstrip()
            proba_list = []
            for i in range(len(f_result_list)):
                proba_list.append((float(f_result_list[i].readline().rstrip().split()[index_list[i]]), i))

            proba_list = sorted(proba_list, key=itemgetter(0), reverse=True)
            if proba_list[1][0] > float(threshold):
                query_dict[query] = ' | '.join(['CLASS=' + CLASS_LIST[proba_c[1]] for proba_c in proba_list[: 2]])
            else:
                query_dict[query] = ' | '.join(['CLASS=' + CLASS_LIST[proba_c[1]] for proba_c in proba_list[: 1]])
    return query_dict

def main():
    if len(sys.argv) != 6:
        print 'Usage: ./gen_final_result.py ../Data/test_query ./predict_results/ threshold ../Data/test.txt ./final_result'
    else:
        query_dict = gen_proba_list(sys.argv[1], sys.argv[2], sys.argv[3])
        gen_final_result(sys.argv[4], sys.argv[5], query_dict)

if __name__ == '__main__':
    main()