#!/usr/bin/python3

import sys
import os
import argparse
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics


def process_console_args():
    parser = argparse.ArgumentParser('hotspot_detector.py')
    parser.add_argument('-f', '--file', metavar='', default=None, help='The path of the file you want to process')
    args = parser.parse_args()
    return args


def main():
    args = process_console_args()
    filepath = args.file
    file_obj = open(filepath, 'rt')
    array = np.zeros((2,2), dtype=int)
    for line in file_obj:
        try:
            if len(line) > 0:
                addr = int(line.split(':')[3][2:18],16)
                array.append([addr, 0], axis = 0)
        except Exception as e:
            print(e)

    print(array)
    return


if __name__ == "__main__":
    main()
