#!/usr/bin/env bash

FILEBASE=$1

head=$2
tail=$3


for i in $(seq 0 3);
do
    for minpts in $(seq 100 100 500);
    do
        echo "========= $FILEBASE${i}_${minpts}_${head}_${tail} =========="
        ./hotspot_detector.py -H $head -T $tail -m $minpts -f $FILEBASE$i -o $FILEBASE${i}_${minpts}_${head}_${tail}.png
    done
done