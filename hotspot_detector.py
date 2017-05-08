#!/usr/bin/python3
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import os
import argparse
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics
import matplotlib.ticker as ticker

def process_console_args():
    parser = argparse.ArgumentParser('hotspot_detector.py')
    parser.add_argument('-f', '--file', metavar='', default=None, help='The path of the file you want to process')
    parser.add_argument('-o', '--output', metavar='', default=None, help='The path of the output file you want to generate')
    parser.add_argument('-e', '--eps', metavar='', default=2048, type=int, help='radius for dbscan')
    parser.add_argument('-m', '--minpts', metavar='', default=100, type=int, help='minimum number of points in the range')
    parser.add_argument('-H', '--headmemaddr', metavar='', default=0x00000000, type=int, help='memory head')
    parser.add_argument('-T', '--tailmemaddr', metavar='', default=0xffffffff, type=int, help='memory tail')
    args = parser.parse_args()
    return args

def formatAddr(x, pos):
    s = '{0:#0{1}X}'.format(x.astype(int),18)
    return s

def main():
    args = process_console_args()
    filepath = args.file
    file_obj = open(filepath, 'rt')
    X = np.empty((0,2),dtype=int)
    v = 1
    for line in file_obj:
        try:
            if len(line) > 0:
                addr = int(line.split(':')[3][10:18],16)
                if addr >= args.headmemaddr and addr < args.tailmemaddr:
                    X = np.append(X, [[v, addr]], axis = 0)
                v = v+1
        except Exception as e:
            print(e)

    if len(X) == 0:
        exit(0)

    db = DBSCAN(8192,50).fit(X)
    # db = DBSCAN(eps=0.05, min_samples=3).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)


    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'

        class_member_mask = (labels == k)

        xy = X[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=14)

        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'x', markerfacecolor=col,
                 markeredgecolor='k', markersize=6)

    plt.title('Estimated number of clusters: %d' % n_clusters_)
    axes = plt.gca()
    axes.get_yaxis().set_major_formatter(ticker.FuncFormatter(formatAddr))
    print('Estimated number of clusters: %d' % n_clusters_)
    # plt.yticks(rotation=30)
    plt.tight_layout()
    plt.show()
    return


if __name__ == "__main__":
    main()
