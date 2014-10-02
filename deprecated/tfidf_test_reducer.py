#!/usr/bin/env python

from itertools import groupby
from operator import itemgetter
import sys

def read_mapper_output(file):
    for line in file:
        yield line.rstrip()


def main():
    '''
        word count reducer
    '''
    data = read_mapper_output(sys.stdin)
    for line in data:
        print line

if __name__ == "__main__":
    main()
