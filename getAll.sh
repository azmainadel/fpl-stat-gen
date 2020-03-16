#!/bin/bash

for i in {1..30}
do 
  python3 python_script/getKoraFPLStat.py -g $i
done
