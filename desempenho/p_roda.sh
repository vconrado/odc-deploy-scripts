#!/bin/bash


if [ $# -lt 3 ]; then
    echo "Usage $(basename $0) teste_label teste #threads"
    exit 1
fi

label=${1:-"label"}
teste=$2
threads=$3


for prod in "ls8_level1_epsg32723_1" "ls8_level1_epsg32723_2" "ls8_level1_epsg32723_3" "ls8_level1_epsg32723_4" "ls8_level1_epsg32723_5"; do
    for teste in "cubo1" "cubo2" "scene1" "scene2" "ts1" "ts2"; do
        echo "Iniciando teste paralelo ${prod}.${teste} #$threads"
        echo "Limpando cache"
        sudo sysctl -w vm.drop_caches=3
        ssh esensing-004 sudo sysctl -w vm.drop_caches=3
        echo "Limpa !"
        echo "Executando $teste $prod"
        docker exec odc-jupyter /datacube/scripts/desempenho/p_testa.sh $label $prod $teste $threads
        echo "Finalizado teste ${prod}.${teste}"
    done
done
echo "Done !!!!"
