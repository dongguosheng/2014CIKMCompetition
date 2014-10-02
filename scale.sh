#!/usr/bin/bash

date


echo "./windows/svm-scale.exe -l 0 ../Data/train_feature > ../Data/train_feature_scale"
./windows/svm-scale.exe -l 0 ../Data/train_feature > ../Data/train_feature_scale


date