#!/bin/bash

for i in "dataset_pepper" "dataset_pepper_enhanced" "dataset_pepper"; do
    mv /host_mount/$i /host_mount/dataset
    /usr/bin/python3 /host_mount/quali.py
    mv /host_mount/dataset /host_mount/$i
    mv /host_mount/neat_results /host_mount/{$i}_neat_results
    mkdir /host_mount/neat_results
done
