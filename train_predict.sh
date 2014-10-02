#!/usr/bin/bash

# train
echo "Begin training models and predict results"

# train models
# 不同的模型具有不同的正负样本比例，需要有不同的模型参数
train_input="train_"

########################################################################################################################
echo "./windows/train.exe -s 1 -c 0.0005 -B 1 -w1 1 -w-1 1 ../Data/train_files/"$train_input"0 ./models/model_0"
./windows/train.exe -s 1 -c 0.0005 -B 1 -w1 1 -w-1 1 ../Data/train_files/"$train_input"0 ./models/model_0

echo "./windows/train.exe -s 1 -c 0.001 -B 1 -w1 2 -w-1 1 ../Data/train_files/"$train_input"1 ./models/model_1"
./windows/train.exe -s 1 -c 0.001 -B 1 -w1 2 -w-1 1 ../Data/train_files/"$train_input"1 ./models/model_1

echo "./windows/train.exe -s 1 -c 0.001 -B 1 -w1 2 -w-1 1 ../Data/train_files/"$train_input"2 ./models/model_2"
./windows/train.exe -s 1 -c 0.001 -B 1 -w1 2 -w-1 1 ../Data/train_files/"$train_input"2 ./models/model_2

echo "./windows/train.exe -s 1 -c 0.001 -B 1 -w1 5 -w-1 1 ../Data/train_files/"$train_input"3 ./models/model_3"
./windows/train.exe -s 1 -c 0.001 -B 1 -w1 5 -w-1 1 ../Data/train_files/"$train_input"3 ./models/model_3

echo "./windows/train.exe -s 1 -c 0.001 -B 1 -w1 15 -w-1 1 ../Data/train_files/"$train_input"4 ./models/model_4"
./windows/train.exe -s 1 -c 0.001 -B 1 -w1 15 -w-1 1 ../Data/train_files/"$train_input"4 ./models/model_4

echo "./windows/train.exe -s 1 -c 0.001 -B 1 -w1 10 -w-1 1 ../Data/train_files/"$train_input"5 ./models/model_5"
./windows/train.exe -s 1 -c 0.001 -B 1 -w1 10 -w-1 1 ../Data/train_files/"$train_input"5 ./models/model_5

echo "./windows/train.exe -s 1 -c 0.001 -B 1 -w1 1 -w-1 1 ../Data/train_files/"$train_input"6 ./models/model_6"
./windows/train.exe -s 1 -c 0.001 -B 1 -w1 1 -w-1 1 ../Data/train_files/"$train_input"6 ./models/model_6
########################################################################################################################
# echo "./windows/train.exe -s 0 -c 0.04 -B 5 -w1 1 -w-1 1 ../Data/train_files/"$train_input"0 ./models/model_0"
# ./windows/train.exe -s 0 -c 0.04 -B 5 -w1 1 -w-1 1 ../Data/train_files/"$train_input"0 ./models/model_0

# echo "./windows/train.exe -s 0 -c 0.04 -B 5 -w1 2 -w-1 1 ../Data/train_files/"$train_input"1 ./models/model_1"
# ./windows/train.exe -s 0 -c 0.04 -B 5 -w1 2 -w-1 1 ../Data/train_files/"$train_input"1 ./models/model_1

# echo "./windows/train.exe -s 0 -c 0.04 -B 5 -w1 1 -w-1 1 ../Data/train_files/"$train_input"2 ./models/model_2"
# ./windows/train.exe -s 0 -c 0.04 -B 5 -w1 1 -w-1 1 ../Data/train_files/"$train_input"2 ./models/model_2

# echo "./windows/train.exe -s 0 -c 0.04 -B 5 -w1 12 -w-1 1 ../Data/train_files/"$train_input"3 ./models/model_3"
# ./windows/train.exe -s 0 -c 0.04 -B 5 -w1 12 -w-1 1 ../Data/train_files/"$train_input"3 ./models/model_3

# echo "./windows/train.exe -s 0 -c 0.04 -B 5 -w1 10 -w-1 1 ../Data/train_files/"$train_input"4 ./models/model_4"
# ./windows/train.exe -s 0 -c 0.04 -B 5 -w1 10 -w-1 1 ../Data/train_files/"$train_input"4 ./models/model_4

# echo "./windows/train.exe -s 0 -c 0.04 -B 5 -w1 2 -w-1 1 ../Data/train_files/"$train_input"5 ./models/model_5"
# ./windows/train.exe -s 0 -c 0.04 -B 5 -w1 2 -w-1 1 ../Data/train_files/"$train_input"5 ./models/model_5

# echo "./windows/train.exe -s 0 -c 0.04 -B 5 -w1 1 -w-1 1 ../Data/train_files/"$train_input"6 ./models/model_6"
# ./windows/train.exe -s 0 -c 0.04 -B 5 -w1 1 -w-1 1 ../Data/train_files/"$train_input"6 ./models/model_6
########################################################################################################################

# predict 
for((i = 0; i < 7; ++i))
do 
    echo "./windows/predict.exe -b 1 ../Data/test_feature ./models/model_"$i" ./predict_results/result_"$i
    ./windows/predict.exe -b 1 ../Data/test_feature ./models/model_""$i ./predict_results/result_""$i
done

# gen final results
echo "./gen_final_result.py ../Data/test_query ./predict_results/ 0.5 ../Data/test.txt ./final_result"
./gen_final_result.py ../Data/test_query ./predict_results/ 0.5 ../Data/test.txt ./final_result

echo "Done"