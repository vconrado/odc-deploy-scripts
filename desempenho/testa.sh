#!/bin/bash

if [ $# -lt 3 ]; then
    echo "Usage: $(basename $0) label product teste"
    exit 1
fi


label=$1
prod=$2
teste=$3

dir="/datacube/scripts/desempenho/dados/$label/"
mkdir -p $dir
python3 /datacube/scripts/desempenho/testa.py $label $prod $teste >> $dir/testa.log
