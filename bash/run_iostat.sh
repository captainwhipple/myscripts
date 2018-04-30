#!/bin/bash
#
# Script to start iostat on several nodes.
# /home/ubuntu/perfstat isn't created, so make sure it is there... or modify the script to do that.

STAT_INTERVAL=$1
STAT_FILE=$2
NODE_FILE=$3

if [[ ! $STAT_INTERVAL || ! $STAT_FILE || ! $NODE_FILE ]]
then
  echo
  echo "USAGE:  run_iostat.sh <interval sec> <output file name>"
  echo "EXAMPLE:  ./run_iostat.sh 2 iostat_20180305.log"
  echo
  exit 1
fi

pssh -h ${NODE_FILE} "nohup iostat -h -y -t -x $1 > /home/ubuntu/perfstat/${STAT_FILE} 2>&1 &"

