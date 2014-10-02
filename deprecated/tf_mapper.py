#!/usr/bin/env python
"""A more advanced Mapper, using Python iterators and generators."""

import sys

def read_session(input):
    '''
    Read a session block, return a tuple, (classes, queries, contents).
    '''
    
    for session in input:
        session_query_list = []
        session_content_list = []
        class_list = []

        for line in session.rstrip().split(','):
            items = line.rstrip().split('\t')

            if len(items) == 2 or items[2] == '-':
                session_query_list.append(items[1])
            else:
                session_query_list.append(items[1])
                session_content_list.append(items[2])

            if 'UNKNOWN' in items[0] or 'TEST' in items[0]:
                pass
            else:
                if '|' in items[0]:
                    class_list.extend(items[0].split(' | '))
                else:
                    class_list.append(items[0])

        # handle classes
        if len(class_list) == 0:
            class_list.append('CLASS=TEST')
        else:
            class_list = list(set(class_list))
            class_list.sort()

        # add query
        session_content_list.extend(session_query_list)

        # querys remove duplicates and sort
        session_query_list = list(set(session_query_list))
        session_query_list.sort()        

        yield (class_list, session_query_list, session_content_list)

def get_term_count_dict(segment_list, n):
    '''
    Return a dict: key => term(n-gram); value => term count.
    '''
    rs_dict = {}
    for segment in segment_list:
        words = segment.split()
        for i in range(1, n + 1):
            for j in range(len(words) - i + 1):
                word = ' '.join(words[j : i + j])
                if word in rs_dict:
                    rs_dict[word] += 1
                else:
                    rs_dict[word] = 1 
    return rs_dict

def gen_format_values(term_count_dict, separator=','):
    '''
    Return string with format (word:term count, word:term count, ...).
    '''
    return separator.join([word + ':' + str(count) for word, count in term_count_dict.items()])

def main(separator='\t'):
    # input comes from STDIN (standard input)
    session_tuples = read_session(sys.stdin)
    for session_tuple in session_tuples:
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        #
        # tab-delimited; the trivial word count is 1

        n = int(sys.argv[1])

        value_str = gen_format_values(get_term_count_dict(session_tuple[2], n))            

        print '%s%s%s' % (','.join(session_tuple[1]), separator, '|'.join(session_tuple[0]) + '+' + value_str)

if __name__ == "__main__":
    main()