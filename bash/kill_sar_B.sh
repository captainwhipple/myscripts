#!/bin/bash

NODEFILE=$1

if [[ ! $NODEFILE ]]
then
  echo "kill_sar_B.sh <node file>"
  echo
  exit
fi

for n in $(cat ${NODEFILE})
do
  echo ".... $n"
  ssh $n "pkill -f 'sar -B'"
done

