#!/usr/bin/bash

source ./venv/bin/activate

for iteration in {1..20}
do
    file="./benchmark_logs/output$iteration.txt"
    python benchmark.py > $file 2>&1
done
