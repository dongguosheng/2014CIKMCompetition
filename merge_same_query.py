#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

CLASS_DICT = {'VIDEO' : 1, 'NOVEL' : 2, 'GAME' : 3, 'TRAVEL' : 4, 'LOTTERY' : 5, 'ZIPCODE' : 6, 'OTHER' : 7, 'TEST' : 8}

def merge_same_query(labeled_file, merged_file):
    '''
    Merge logs with same query.
    Doc Dict: key => query, value => [Title Dict, Class List].
    Title Dict: key => title, value => count.
    '''
    doc_dict = {}
    with open(labeled_file) as f:
        for line in f:
            if line == '\n':
                continue
            temp_list = line.rstrip().split('\t')
            query = temp_list[1]
            if query not in doc_dict:
                doc_dict[query] = [{}, set()]
            for c, num in CLASS_DICT.items():
                if c in temp_list[0]:
                    doc_dict[query][1].add(str(num))
            if len(temp_list) > 2 and temp_list[2] != '-':
                if temp_list[2] not in doc_dict[query][0]:
                    doc_dict[query][0][temp_list[2]] = 1
                else:
                    doc_dict[query][0][temp_list[2]] += 1

    f_out = open(merged_file, 'w')
    for query, value_list in doc_dict.items():
        f_out.write(query + '\t')
        f_out.write(','.join([title + ':' + str(count) for title, count in value_list[0].items()]) + '\t')
        f_out.write(','.join(list(value_list[1])) + '\n')
    f_out.close()

def main():
    if len(sys.argv) != 3:
        print 'Usage: ./merge_same_query.py ../Data/labeled_file ../Data/merged_file'
    else:
        merge_same_query(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()