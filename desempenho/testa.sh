#!/bin/bash

if [ $# -lt 3 ]; then
    echo "Usage: $(basename $0) label product teste [#threads]"
    exit 1
fi


label=$1
prod=$2
teste=$3
threads=$4

dir="/datacube/scripts/desempenho/dados/$label/"
mkdir -p $dir
python3 /datacube/scripts/desempenho/testa.py $label $prod $teste $threads >> $dir/testa.log
