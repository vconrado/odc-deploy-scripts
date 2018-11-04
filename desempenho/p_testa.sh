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
    dir="/datacube/scripts/desempenho/dados/$label/$i"
    mkdir -p $dir
    python3 /datacube/scripts/desempenho/testa.py "$label/$i" $prod $teste >> $dir/${t_label}.log & 
    pids[${i}]=$!
    echo "Iniciando thread ${label}-${i} $prod $teste PID " $pids[${i}]
done

echo "Esperando finalizar processos"
for pid in ${pids[*]}; do
    wait $pid
    echo "Processo $pid finalizado" 
done
