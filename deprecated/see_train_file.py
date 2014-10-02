#!/usr/bin/python
# -*- coding: utf-8 -*-

def filter_test(threshold=2000):
    '''
    See content besides TEST class.
    '''
    line_num = 0
    with open('train_sessions') as f:
        for line in f:
            if 'TEST' in line:
                # continue
                line_num += 1
                print line.strip()
            else:
                line_num += 1
                print line.strip()

            if line_num > threshold:
                break

def main():
    filter_test()

if __name__ == '__main__':
    main()