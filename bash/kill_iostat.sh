#!/bin/bash

NODEFILE=$1

if [[ ! $NODEFILE ]]
then
  echo 'kill_iostat.sh <node file>'
  echo
  exit
fi

for n in $(cat ${NODEFILE})
do
echo ".......... $n"
ssh $n "pkill -f 'iostat -h -y -t -x 5'"
done

