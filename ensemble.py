#!/usr/bin/env python

# -*- coding: utf-8 -*-

WEIGHT_LIST = [
                [0.5, 0.5],
                [0.5, 0.5],
                [0.5, 0.5],
                [0.5, 0.5],
                [0.5, 0.5],
                [0.5, 0.5],
                [0.5, 0.5]
                # [0.9240, 0.9241],
                # [0.9628, 0.9631],
                # [0.9681, 0.9692],
                # [0.9947, 0.9948],
                # [0.9988, 0.9990],
                # [0.9990, 0.9990],
                # [0.9126, 0.9122]
              ]

import sys
from operator import itemgetter
import os

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

def gen_proba_list(test_query, result_dir_list, threshold):
    query_dict = {}
    for result_dir in result_dir_list:
        if result_dir[-1] != '/':
            result_dir += '/'

    f_result_list = []
    for i in range(7):
        f_list = []
        for result_dir in result_dir_list:
            f_list.append(open(result_dir + 'result_' + str(i)))

        f_result_list.append(f_list)

    index_list = []
    for f_list in f_result_list:
        temp_index_list = []
        for f in f_list:
            temp_list = f.readline().rstrip().split()
            temp_index_list.append(temp_list.index('1'))
        index_list.append(temp_index_list)

    with open(test_query) as f:
        cnt = 0
        for line in f:
            query = line.rstrip()
            proba_list = []
            for i in range(len(f_result_list)):
                ensemble_proba = 0.0
                weight_sum = 0.0
                temp_proba_list = []
                for j in range(len(f_result_list[i])):
                    proba = float(f_result_list[i][j].readline().rstrip().split()[index_list[i][j]])
                    temp_proba_list.append(proba)
                    ensemble_proba += WEIGHT_LIST[i][j] * proba
                    weight_sum += WEIGHT_LIST[i][j]

                if (temp_proba_list[0] > 0.5 and temp_proba_list[1] < 0.5) or (temp_proba_list[0] < 0.5 and temp_proba_list[1] > 0.5):
                    cnt += 1
                    print temp_proba_list

                proba_list.append((ensemble_proba / weight_sum, i))

            proba_list = sorted(proba_list, key=itemgetter(0), reverse=True)
            if proba_list[1][0] > float(threshold):
                query_dict[query] = ' | '.join(['CLASS=' + CLASS_LIST[proba_c[1]] for proba_c in proba_list[: 2]])
            else:
                query_dict[query] = ' | '.join(['CLASS=' + CLASS_LIST[proba_c[1]] for proba_c in proba_list[: 1]])
        print cnt
    return query_dict

def get_dir_list(root):
    if root[-1] != '/':
        root += '/' 
    rs_list = []
    dirs = os.listdir(root)
    for d in dirs:
        rs_list.append(root + d + '/')

    return rs_list

def main():
    if len(sys.argv) != 6:
        print 'Usage: ./ensemble.py ../Data/test_query ./ensemble/ threshold ../Data/test.txt ./final_result'
    else:
        dir_list = get_dir_list(sys.argv[2])
        query_dict = gen_proba_list(sys.argv[1], dir_list, sys.argv[3])
        gen_final_result(sys.argv[4], sys.argv[5], query_dict)

if __name__ == '__main__':
    main()