#!/usr/bin/env python
"""A more advanced Mapper, using Python iterators and generators."""

import sys
import math
from operator import itemgetter

def read_doc(input):
    '''
    Read a session block, return a tuple, (queries, contents).
    '''
    for line in input:
        yield line.rstrip().split('\t')

def resume_dict(value_str):
    '''
    Resume string with format (word:term count, word:term count, ...) to dict.
    '''
    rs_dict = {}
    for item in value_str.rstrip().split(','):
        term_count = item.split(':')
        try:
            rs_dict[term_count[0]] = int(term_count[1])
            # print item
        except IndexError, e:
            sys.stderr.write(item)
            sys.stderr.write(' IndexError.\n')

    return rs_dict

def cal_tfidf(tf_dict):
    rs_dict = {}
    # term_count = float(len(tf_dict))
    for word, tf in tf_dict.items():
        if word in idf_dict:
            rs_dict[index_dict[word]] = round(idf_dict[word] * (1 + math.log(float(tf))), 6) # / idf * (1 + log(tf))
    return sorted(rs_dict.iteritems(), key=itemgetter(0))

def gen_format_values(tfidf_list, separator=' '):
    '''
    Return string with format (word:term count, word:term count, ...).
    '''
    return separator.join([str(index) + ':' + str(tfidf) for index, tfidf in tfidf_list])

# initialize a global df dict, query table and class label
# print 'initialize start.'
class_dict = {'VIDEO' : 1, 'NOVEL' : 2, 'GAME' : 3, 'TRAVEL' : 4, 'LOTTERY' : 5, 'ZIPCODE' : 6, 'OTHER' : 7, 'TEST' : 8}

total_doc = 2634606.0

idf_dict = {}
index_dict = {}
index = 1
with open('df_3gram_filtered.txt') as f:
    for line in f:
        temp_list = line.rstrip().split('\t')
        idf_dict[temp_list[0]] = math.log(total_doc / (float(temp_list[1]) + 1))
        index_dict[temp_list[0]] = index
        index += 1
# print 'initialize complete.'

def main(separator='\t'):   
    # input comes from STDIN (standard input)
    docs = read_doc(sys.stdin)
    for doc in docs:
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        #
        # tab-delimited; the trivial word count is 1
        tf_dict = resume_dict(doc[1].rstrip().split('+')[-1])
        class_str = doc[1].rstrip().split('+')[0]
        
        class_num_list = []
        if 'TEST' not in class_str:
            for key, value in class_dict.items():
                if key in class_str:
                    class_num_list.append(str(value))
            print '%s%s%s' % (doc[0], separator, '|'.join(class_num_list) + ' ' + gen_format_values(cal_tfidf(tf_dict)))

if __name__ == "__main__":
    main()