# -*- coding: utf-8 -*-
#!/usr/bin/env python

def df_filter(df=10):
    with open('df_filtered.txt', 'w') as f:
        with open('df.txt') as f_:
            for line in f_:
                if int(line.rstrip().split()[-1]) >= df:
                    f.write(line)

def main():
    df_filter()

if __name__ == '__main__':
    main()