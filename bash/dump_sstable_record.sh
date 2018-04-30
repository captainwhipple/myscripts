#!/bin/bash
# 
# Runs sstabledump for a database record of interest
# ./dump_sstable_record.sh <keyspace> <table> <primary_key>

KYSP=$1
TBL=$2
PK=$3

if [[ ! $KYSP || ! $TBL || ! $PK ]]
then
   echo "dump_sstable_record.sh <keyspace> <table> <primary_key>"
   exit 1
fi


for n in $(ssh $(head -1 /home/ubuntu/admin/control/allnodes) "nodetool getendpoints -- $KYSP $TBL $PK")
do
  echo "......... $n"
  echo ">>>> flushing table"
  ssh $n "nodetool flush -- $KYSP $TBL"
  SSTAB=$(ssh $n "nodetool getsstables -- $KYSP $TBL $PK")
  echo ">>>> sstable: $SSTAB"
  ssh $n "sstabledump $SSTAB -k $PK"
done

echo ".... el fin"
