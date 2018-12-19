#!/bin/sh
if [ -z "$1" ]
  then
    num_iterations=1000
  else
    num_iterations=$1
fi

for i in `seq 1 $num_iterations`;
do
        echo "--- Iteration #$i out of $num_iterations:---"
	python3 /root/connectin/migration_scripts/mssql_to_influx.py
done
