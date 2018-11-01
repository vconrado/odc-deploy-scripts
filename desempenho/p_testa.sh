#!/bin/bash

if [ $# -lt 4 ]; then
    echo "Usage: $(basename $0) label product teste #threads"
    exit 1
fi


label=$1
prod=$2
teste=$3
threads=$4



for i in $(seq 1 $threads); do
    t_label="${label}_t-${i}"
    dir="/datacube/scripts/desempenho/dados/$t_label"
    mkdir -p $dir
    python3 /datacube/scripts/desempenho/testa.py $t_label $prod $teste >> $dir/${t_label}.log 
done
