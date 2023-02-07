#!/usr/bin/bash

source ./venv/bin/activate

graphID=0

for src in {0..6}
do
    for dest in {0..6}
    do
        if [ $src -ne $dest ]
        then
            python Experiment.py $graphID -src $src -dest $dest
            cat comm_template.json
        fi
    done
done