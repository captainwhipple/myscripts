for n in $(cat ~/allnodes)
do
ssh $n sudo "sed -i -e '\$aagent_rpc_broadcast_address: $n' /var/lib/datastax-agent/conf/address.yaml"
done
