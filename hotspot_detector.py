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
    parser.add_argument('-o', '--output', metavar='', default=None, help='The path of the output file you want to generate')
    parser.add_argument('-e', '--eps', metavar='', default=2048, type=int, help='radius for dbscan')
    parser.add_argument('-m', '--minpts', metavar='', default=100, type=int, help='minimum number of points in the range')
    parser.add_argument('-H', '--headmemaddr', metavar='', default=0x00000000, type=int, help='memory head')
    parser.add_argument('-T', '--tailmemaddr', metavar='', default=0xffffffff, type=int, help='memory tail')
    args = parser.parse_args()
    return args


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
    db = DBSCAN(eps=args.eps, min_samples=args.minpts).fit(X)
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


    cluster_table = np.full((n_clusters_, len(labels)), -1, dtype = int)
    for inst_idx in range(len(db.components_)):
        addr = db.components_[inst_idx][1]
        label_idx = db.core_sample_indices_[inst_idx]
        inst_label = labels[label_idx]
        cluster_table[inst_label, label_idx] = addr

    clst_name=[]
    for cluster_idx in range(n_clusters_):
        min = 0xffffffff
        max = 0x00000000
        num_inst = 0
        for addr_ in cluster_table[cluster_idx]:
            if addr_ >= 0x00000000:
                num_inst = num_inst + 1
                if min > addr_:
                    min = addr_
                if max < addr_:
                    max = addr_
        clst_name.append("C{:02}({}~{}, inst={})".format(cluster_idx,"{0:#0{1}X}".format(min,18),"{0:#0{1}X}".format(max,18), num_inst))
        print("For cluster ", "{:02}".format(cluster_idx), ", the range = (", "{0:#0{1}X}".format(min,18), " ~ ", "{0:#0{1}X}".format(max,18), "), number of instances = ", num_inst)


    num_outlier = 0
    for label_ in labels:
        if label_ == -1:
            num_outlier = num_outlier + 1

    plot_title = "{}, num_clusters={}, \nnum_outliers={}/{}, num_core_samples={}/{}"\
        .format(args.output, n_clusters_, num_outlier, len(labels), len(db.core_sample_indices_), len(labels))
    print("The total number of outliers = ", num_outlier, ", the number of all core samples = ", len(db.core_sample_indices_), ", the number of all instances =", len(labels))



    # print("Silhouette Coefficient: %0.3f"
    #       % metrics.silhouette_score(X, labels))

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    clst = []
    markr = "o"
    for k, col in zip(unique_labels, colors):
        class_member_mask = (labels == k)
        if k == -1:
            # Black used for noise.
            col = 'k'
            markr = 'x'
            xy = X[class_member_mask & ~core_samples_mask]
            plt.scatter(xy[:, 0], xy[:, 1], c=col, marker=markr)

        xy = X[class_member_mask & core_samples_mask]
        clst.append(plt.scatter(xy[:, 0], xy[:, 1], c=col, marker=markr))

    plt.legend(clst, clst_name, loc='upper center', bbox_to_anchor=(0.5,-0.1))
    # plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.title(plot_title)
    plt.savefig(args.output)


    return


if __name__ == "__main__":
    main()
