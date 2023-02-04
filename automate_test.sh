#!/usr/bin/bash

source ./venv/bin/activate

for iteration in {1..20}
do
    python -m unittest -v test_incremental.py 2>> output.txt
done
