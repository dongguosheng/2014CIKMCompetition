#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def cal_df(input_file, df_file, n, threshold):
    df_dict = {}
    with open(input_file) as f:
        for line in f:
            word_set = set()
            query, titles, class_str = line.rstrip().split('\t')
            segments = [query]
            segments.extend(title_count.split(':')[0] for title_count in titles.split(','))
            for segment in segments:
                words = segment.split()
                for i in range(1, int(n) + 1):
                    for j in range(len(words) - i + 1):
                        word = ' '.join(words[j : i + j])
                        word_set.add(word) 

                # add 4 end gram , which is the best
                # From Zhouxing
                grams = []
                if len(words) > 0:
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
                        word_set.add(gram)

            for word in word_set:
                if word in df_dict:
                    df_dict[word] += 1
                else:
                    df_dict[word] = 1

    with open(df_file, 'w') as f:
        for word, count in df_dict.items():
            if count >= int(threshold):
                f.write(word + '\t' + str(count) + '\n')

def main():
    if len(sys.argv) != 5:
        print 'Usage: ./gen_df.py ../Data/merged_file ../Data/df_file 3 3'
    else:
        cal_df(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == '__main__':
    main()        
