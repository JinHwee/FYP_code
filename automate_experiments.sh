#!/usr/bin/bash

source ../venv/bin/activate

graphID=0

for src in {0..6}
do
    for dest in {0..6}
    do
        if [ $src -ne $dest ]
        then
            python Experiment.py $graphID -src $src -dest $dest
            now=$(date +"%T")
            file=./peer/comm_template.json
            if [ -f "$file" ];
            then
                cat "${file}"
                sudo docker compose up --force-recreate --build node1 node2 node3 node4 node5 node6 node7 --remove-orphans > "./logs/run_log_${now}.txt" 2>&1
            fi
        fi
    done
done
