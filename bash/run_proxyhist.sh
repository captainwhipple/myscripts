#!/bin/bash

for n in $(cat ~/allnodes)
do
echo ".......... $n"
ssh $n 'nodetool proxyhistograms > /home/ubuntu/$(hostname -i)_proxyhist_20180430'
done

