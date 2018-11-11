#!/bin/bash

if [ $# -lt 2 ]; then
	echo "Falta paramentros"
	exit 1
fi


LABEL=$1
LOOPS=$2
#BASE="/mnt/efs"
BASE="/data/ODC/data/scripts/desempenho/aws"
for l in $(seq 1 $LOOPS); do
	FILE="${BASE}/dados/${LABEL}_${l}"
	LOG="${BASE}/logs/${LABEL}_${l}.log"
	dd bs=1M count=1024 if=/dev/zero of=$FILE > $LOG 2>&1 &
	pids[${i}]=$!
	echo "Iniciado $l"
done


echo "Esperando finalizar processos"
for pid in ${pids[*]}; do
    wait $pid
    echo "Processo $pid finalizado" 
done


