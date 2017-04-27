#!/usr/bin/python3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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
    X = np.empty((0,2),dtype=int)
    for line in file_obj:
        try:
            if len(line) > 0:
                addr = int(line.split(':')[3][2:18],16)
                X = np.append(X, [[addr, 0]], axis = 0)
        except Exception as e:
            print(e)

    db = DBSCAN(eps=0.3, min_samples=10).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    print('Estimated number of clusters: %d' % n_clusters_)
    # print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
    # print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
    # print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
    # print("Adjusted Rand Index: %0.3f"
    #       % metrics.adjusted_rand_score(labels_true, labels))
    # print("Adjusted Mutual Information: %0.3f"
    #       % metrics.adjusted_mutual_info_score(labels_true, labels))
    print("Silhouette Coefficient: %0.3f"
          % metrics.silhouette_score(X, labels))

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
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=6)

    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.savefig("foo.png")


    return


if __name__ == "__main__":
    main()
