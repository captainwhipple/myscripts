#!/bin/bash

NODEFILE=$1
FREQ=$2
OUTFILE=$3

if [[ ! $NODEFILE || ! $FREQ ]]
then
  echo "run_sar_B.sh <node file> <poll interval> <output file name>"
  echo "ie: run_sar_B.sh ~/allnodes 30 sar_B_20180426"
  echo 
  exit 0
fi

for n in $(cat $NODEFILE)
do
  echo "... $n"
  ssh $n "nohup sar -B $FREQ > /home/ubuntu/perfstat/${OUTFILE} 2>&1 &"
done
