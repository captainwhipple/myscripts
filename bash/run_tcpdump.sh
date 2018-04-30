#!/bin/bash
#
# Simple script to run tcpdump on multiple servers. Listens for a specific port.

NODES_FILE=$1
TRACE_PORT=$2
# This directory isn't created, so make sure it is there... or modify the script to create it
PCAP_FILE=/home/ubuntu/network_data/tcpdump_$(date +%Y%m%d)_0

if [[ ! $NODES_FILES || ! $TRACE_PORT ]]
do
   echo "run_tcpdump.sh <path_to_node_file> <port>"
   exit 1
done

echo "... starting tcpdump -i ens3 port $TRACE_PORT -w $PCAP_FILE -C 50"
for n in $(cat $NODES_FILE)
do
  echo "... $n"
  ssh $n "sudo -b nohup tcpdump -i ens3 port $TRACE_PORT -w $PCAP_FILE -C 50 > /dev/null 2>&1"
done

echo "... listing tcpdump processes"
pssh -h $NODES_FILE --print "ps -ef|grep tcpdump"
