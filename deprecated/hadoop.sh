# cal tf, n-gram
hadoop jar $hadoop_streaming -input ./train_sessions -output ./tf -mapper "tf_mapper.py 3" -reducer "tf_reducer.py" -file tf_mapper.py -file tf_reducer.py

# cal df
hadoop jar $hadoop_streaming -input ./tf/part-00000 -output ./df -mapper "df_mp.py" -reducer "df_rd.py 10" -file df_mp.py -file df_rd.py

pan -get ./df_3gram/part-00000 ./df_3gram.txt

# cal total doc num
hadoop jar $hadoop_streaming -input ./tf/part-00000 -output ./total_doc -mapper "total_doc_mp.py" -reducer "total_doc_rd.py" -file total_doc_mp.py -file total_doc_rd.py

# cal train tfidf
hadoop jar $hadoop_streaming -input ./tf_3gram/part-00000 -output ./tfidf_train_filtered -mapper "tfidf_train_mapper.py" -file tfidf_train_mapper.py -reducer "tfidf_train_reducer.py" -file tfidf_train_reducer.py -file df_3gram_filtered.txt

# cal test tfidf
hadoop jar $hadoop_streaming -input ./tf_3gram/part-00000 -output ./tfidf_test_filtered -mapper "tfidf_test_mapper.py" -file tfidf_test_mapper.py -reducer "tfidf_test_reducer.py" -file tfidf_test_reducer.py -file df_3gram_filtered.txt

# feature selection
hadoop jar QueryDetection.jar com.guosheng.featureSelection.CalClassDocNum ./tfidf_3gram_train/part-00000 ./class_doc_num/

hadoop jar $hadoop_streaming -input ./tfidf_3gram_train/part-00000 -output ./df_3gram_train -mapper "df_mp_train.py" -reducer "df_rd_train.py" -file df_mp_train.py -file df_rd_train.py

hadoop jar QueryDetection.jar com.guosheng.featureSelection.CalClassDocNumWithFeature ./tfidf_3gram_train/part-00000 ./class_doc_num_with_feature/


# train and predict
hadoop jar QueryDetection.jar com.guosheng.svm.SVMClassifier ./tfidf_train_filtered/part-00000 ./tfidf_test_filtered/part-00000 ./predict/

#--------------------------------------------------------------#
# copy tfidf file
hadoop fs -copyToLocal ./tfidf_3gram/part-0000* ./tfidf_part1/

# copy tfidf zip to hdfs
hadoop fs -copyFromLocal ./tfidf_part#.zip ./tfidf_#gram_zip/