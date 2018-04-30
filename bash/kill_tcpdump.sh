#!/bin/bash
#
# Script to stop tcpump sessions on multiple servers

NODE_FILE=$1

if [[ ! $NODE_FILE ]]
then
  echo "USAGE: kill_tcpdump.sh <node list file>"
  exit
fi

for n in $(cat $NODE_FILE)
do
  echo "... on $n running sudo pkill --signal SIGKILL tcpdump"
  ssh $n sudo pkill --signal SIGKILL tcpdump
done

