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
    file_obj = open(file_path, 'rt')
    for line in file_obj:
		try:
			if len(line) > 0:
				print(line)
		except Exception as e:
			print(e)
	return


if __name__ == "__main__":
    main()
