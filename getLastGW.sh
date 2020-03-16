#!/bin/bash

echo "Enter last GW number: "

read lastGW
i=30

python3 python_script/getKoraFPLStat.py -g $lastGW
