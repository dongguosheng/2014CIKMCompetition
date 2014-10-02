#!/usr/bin/env python
"""A more advanced Reducer, using Python iterators and generators."""

from itertools import groupby
from operator import itemgetter
import sys

def read_mapper_output(input, separator='\t'):
    for line in input:
        yield line.rstrip().split(separator, 1)

def gen_format_values(term_count_dict, separator=','):
    '''
    Return string with format (word:term count, word:term count, ...).
    '''
    return separator.join([word + ':' + str(count) for word, count in term_count_dict.items()])

def resume_dict(value_str):
    '''
    Resume string with format (word:term count, word:term count, ...) to dict.
    '''
    rs_dict = {}
    for item in value_str.rstrip().split(','):
        term_count = item.split(':')
        rs_dict[term_count[0]] = int(term_count[1])

    return rs_dict

def merge_dict(term_count_dict, temp_dict):
    for key_temp, value_temp in temp_dict.items():
        if key_temp in term_count_dict:
            term_count_dict[key_temp] += value_temp
        else:
            term_count_dict[key_temp] = value_temp
    return term_count_dict

def main(separator='\t'):
    # input comes from STDIN (standard input)
    data = read_mapper_output(sys.stdin, separator=separator)
    # groupby groups multiple word-count pairs by word,
    # and creates an iterator that returns consecutive keys and their group:
    #   current_word - string containing a word (the key)
    #   group - iterator yielding all ["&lt;current_word&gt;", "&lt;count&gt;"] items
    for doc_key, group in groupby(data, itemgetter(0)):
        try:
            term_count_dict = {}
            class_list = []
            for current_word, value in group:
                value_list = value.rstrip().split('+')
                if len(value_list) < 2:
                    pass
                else:
                    temp_dict = resume_dict(value_list[-1])
                    term_count_dict = merge_dict(term_count_dict, temp_dict)
                class_list.extend(value_list[0].split('|'))
                class_list = list(set(class_list))
            # for test
            # if len(doc_key) == 0:
                # print doc_key, group

            print "%s%s%s" % (doc_key, separator, '|'.join(class_list) + '+' + gen_format_values(term_count_dict))
        except ValueError:
            # count was not a number, so silently discard this item
            pass

if __name__ == "__main__":
    main()