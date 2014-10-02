#!/usr/bin/env python

import math

print 'initialize start.'

# total_doc = 2634606.0
total_doc = 1535350.0    # train

# DF INIT
df_dict = {}
with open('df_3gram_train.txt') as f:
    for line in f:
        temp_list = line.rstrip().split('\t')
        df_dict[temp_list[0]] = float(temp_list[1])

# Class Doc Num
entropy_HD = 0.0
class_doc_num_dict = {'1': 740625, '2': 174739, '3': 230567, '4': 106743, '5': 24897, '6': 4790, '7': 252989}
for key, value in class_doc_num_dict.items():
    entropy_HD += -(float(value) / total_doc) * math.log(float(value) / total_doc)

print 'H(D): ' + str(entropy_HD)

# Class Doc Num With Feature
class_doc_num_with_feature_dict = {}
with open('class_doc_num_with_feature.txt') as f:
    for line in f:
        temp_list = line.rstrip().split()
        if temp_list[0] not in class_doc_num_with_feature_dict:
            class_doc_num_with_feature_dict[temp_list[0]] = {}
        class_doc_num_with_feature_dict[temp_list[0]][temp_list[1]] = float(temp_list[2])

print 'initialize complete.'

print 'cal info gain dict.'
# Cal H(D|A)
entropy_HDA_dict = {}
for feature_index, df in df_dict.items():
    entropy_HDA_in = 0.0
    entropy_HDA_out = 0.0
    if feature_index not in class_doc_num_with_feature_dict:
        print 'feature_index not in ' + feature_index
        pass
    else:
        for label, count in class_doc_num_with_feature_dict[feature_index].items():
            entropy_HDA_in += count / df * math.log(count / df)
            entropy_HDA_out += (class_doc_num_dict[label] - count) / (total_doc - df) * math.log((class_doc_num_dict[label] - count) / (total_doc - df))

        entropy_HDA_in *= -df / total_doc
        entropy_HDA_out *= -(total_doc - df) / total_doc

        entropy_HDA_dict[feature_index] = entropy_HDA_in + entropy_HDA_out

        print feature_index, (entropy_HDA_in + entropy_HDA_out)
