#!/usr/bin/env bash

FILEBASE=$1

for i in $(seq 0 3);
do
    for minpts in $(seq 100 100 500);
    do
        for head in $(seq 0 1000000 5000000000);
        do
            tail=`echo "$head + 1000000"|bc`
            echo "========= $FILEBASE${i}_${minpts}_${head}_${tail} =========="
            ./hotspot_detector.py -h $head -t $tail -m $minpts -f $FILEBASE$i -o $FILEBASE${i}_${minpts}_${head}_${tail}.png
        done
    done
done