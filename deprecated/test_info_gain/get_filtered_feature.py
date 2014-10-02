#!/usr/bin/env python

index_set = set()

def get_feature_index(threshold=0.5):
    with open('entropy.txt') as f:
        for line in f:
            temp_list = line.rstrip().split()
            if float(temp_list[1]) < threshold:
                index_set.add(temp_list[0])

def filter_features():
    with open('df_3gram_filtered.txt', 'w') as f_out:
        with open('df_3gram.txt') as f:
            index = 1
            for line in f:
                index += 1
                if str(index) in index_set:
                    f_out.write(line)

def main():
    get_feature_index()

    filter_features()

if __name__ == '__main__':
    main()