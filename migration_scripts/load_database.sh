#!/bin/sh
for i in `seq 1 1000`;
do
        echo "--- Iteration #$i:---"
	python3 mssql_to_influx.py
done
