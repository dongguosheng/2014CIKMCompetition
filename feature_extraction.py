#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from operator import itemgetter
import math

TOTAL_DOC = 77704

idf_dict = {}
index_dict = {}

# w2v expand
query_expand_dict = {}
num_query_expand = 0

def load_query_expand(query_expand_file):
    '''
    Load query expand file query(word_word)\texpands(word_word).
    '''
    with open(query_expand_file) as f:
        for line in f:
            query, expand = line.rstrip().split('\t')
            expand_list = expand.split()

            if query[-1] != '#':
                query = query.replace('_', ' ')

            for i in range(len(expand_list)):
                if expand_list[i][-1] != '#':
                    expand_list[i] = expand_list[i].replace('_', ' ')

            query_expand_dict[query] = expand_list

    print 'Load query expand Complete.'

def load_df(df_file):
    '''
    Load idf dict from file.
    '''
    index = 1
    with open(df_file) as f:
        for line in f:
            temp_list = line.rstrip().split('\t')
            idf_dict[temp_list[0]] = math.log(TOTAL_DOC / (float(temp_list[1]) + 1))
            index_dict[temp_list[0]] = index
            index += 1
    print 'Load DF Complete.'

def cal_doc_tfidf(line, n):
    '''
    Cal tf vector of doc.
    '''
    tf_dict = {}
    query, titles, class_str = line.rstrip().split('\t')

    # get query tf dict
    query_tf_dict = cal_segment_tf(query, n)

    # expand query
    # max top 10 ALL EXPAND!!!
    # Only expand querys that number of words <= 4

    if query in query_expand_dict:
        global num_query_expand
        num_query_expand += 1
        expand_list = query_expand_dict[query][: 5]
        for i in range(len(expand_list)):
            if expand_list[i] not in query_tf_dict:
                query_tf_dict[expand_list[i]] = 1 - float(i + 1) / 10

    max_count = 0
    for title, count in [(title_count.split(':')[0], int(title_count.split(':')[1])) for title_count in titles.split(',') if len(title_count) > 0]:
        # count 的分布需要统计一下

        # 尝试设置title权重
        weight = 1.0 + math.log(count)  # 对点击数取log  
        # weight = count # 点击数作为weight
        # weight = 1
        title_tf_dict = multiply_weight(cal_segment_tf(title, n), weight)
        for word, tf in title_tf_dict.items():
            if word in tf_dict:
                tf_dict[word] += tf
            else:
                tf_dict[word] = tf
        
        # 设置query中的tf权重
        for word, _ in query_tf_dict.items():
            query_tf_dict[word] += count * 30    # 出现一个种类的title query tf + 1

    for word, tf in query_tf_dict.items():
        if word in tf_dict:
            tf_dict[word] += tf
        else:
            tf_dict[word] = tf

    # cal tfidf
    tfidf_dict = {}
    # cal max tf
    tf_max = 0
    for word, tf in tf_dict.items():
        if tf > tf_max:
            tf_max = tf

    for word, tf in tf_dict.items():
        if word in idf_dict:
            tfidf_dict[index_dict[word]] = (0.2 + 0.8 * tf / tf_max) * idf_dict[word]
    return (query, class_str, sorted(tfidf_dict.iteritems(), key=itemgetter(0)))

def multiply_weight(tf_dict, weight):
    for word, count in tf_dict.items():
        tf_dict[word] = weight * count
    return tf_dict

def cal_segment_tf(segment, n):
    rs_dict = {}
    words = segment.split()
    for i in range(1, n + 1):
        for j in range(len(words) - i + 1):
            word = ' '.join(words[j : i + j])
            if word in rs_dict:
                rs_dict[word] += 1
            else:
                rs_dict[word] = 1

    # add 4 end gram , which is the best
    # From Zhouxing
    grams = []
    grams.append(words[-1]+'#')
    if len(words) > 1:
        grams.append(words[-2]+'_'+words[-1]+'#')
    if len(words) > 2:
        grams.append(words[-3]+'_'+grams[-1])
    if len(words) > 3:
        grams.append(words[-4]+'_'+grams[-1])
    if len(words) > 4:
        grams.append(words[-5]+'-'+grams[-1])
    for gram in grams:
        if gram in rs_dict:
            rs_dict[gram] += 1
        else:
            rs_dict[gram] = 1
    return rs_dict

def extract_feature(merged_file, df_file, train_feature, train_query, test_feature, test_query, n):
    load_df(df_file)
    f_train = open(train_feature, 'w')
    f_test = open(test_feature, 'w')
    f_test_query = open(test_query, 'w')
    f_train_query = open(train_query, 'w')
    with open(merged_file) as f:
        for line in f:
            query, class_str, tfidf_tuple_list = cal_doc_tfidf(line, int(n))
            if '8' in class_str:
                f_test_query.write(query + '\n')
                f_test.write(class_str + '\t' + ' '.join([str(tfidf_tuple[0]) + ':' + str(tfidf_tuple[1]) for tfidf_tuple in tfidf_tuple_list]) + '\n')
            else:
                f_train_query.write(query + '\n')
                f_train.write(class_str + '\t' + ' '.join([str(tfidf_tuple[0]) + ':' + str(tfidf_tuple[1]) for tfidf_tuple in tfidf_tuple_list]) + '\n')

    f_train.close()
    f_test.close()
    f_train_query.close()
    f_test_query.close()

def main():
    if len(sys.argv) != 8:
        print 'Usage: ./feature_extraction.py merged_file df_file train_feature train_query test_feature test_query 4'
    else:
        load_query_expand('../Data/test_query_expand')
        extract_feature(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
        print 'Number of expanded queries: %d' % num_query_expand

if __name__ == '__main__':
    main()