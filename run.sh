#!/usr/bin/bash

date
# preprocessing
# echo "./preprocessing.py ../Data/train ../Data/labeled_file ../Data/unknown_file"
# ./preprocessing.py ../Data/train ../Data/labeled_file ../Data/unknown_file

# # merge same query
# echo "./merge_same_query.py ../Data/labeled_file ../Data/merged_file"
# ./merge_same_query.py ../Data/labeled_file ../Data/merged_file

# gen df file

n=4
threshold=7

# echo "./gen_df.py ../Data/merged_file ../Data/df_file ""$n ""$threshold"
# ./gen_df.py ../Data/merged_file ../Data/df_file $n $threshold

# cal tfidf
echo "./feature_extraction.py ../Data/merged_file ../Data/df_file ../Data/train_feature ../Data/train_query ../Data/test_feature ../Data/test_query ""$n"
./feature_extraction.py ../Data/merged_file ../Data/df_file ../Data/train_feature ../Data/train_query ../Data/test_feature ../Data/test_query ""$n

train_feature="train_feature"

# # scale train data
# ./scale.sh
# train_feature="train_feature_scale"

# gen train files
echo "./gen_train_files.py ../Data/"$train_feature
./gen_train_files.py ../Data/""$train_feature


./train_predict.sh

date