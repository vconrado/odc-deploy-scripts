#!/bin/bash

if [ $# -lt 2 ]; then
	echo "Falta paramentros"
	exit 1
fi


LABEL=$1
LOOPS=$2
BASE="/mnt/efs"

for l in $(seq 1 $LOOPS); do
	FILE="${BASE}/dados/${LABEL}_${l}"
	LOG="${BASE}/logs/read_${LABEL}_${l}.log"
	./leitura $FILE >> $LOG &
	pids[${i}]=$!
	echo "Iniciado $l"
done


echo "Esperando finalizar processos"
for pid in ${pids[*]}; do
    wait $pid
    echo "Processo $pid finalizado" 
done


