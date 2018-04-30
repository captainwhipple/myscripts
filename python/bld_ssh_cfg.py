# Recreates the .ssh/config 
# 1st add curent public names to allnodes
# python3 bld_ssh_cfg.py

import os
import time

allnodes = '/home/ubuntu/allnodes'
sshcfg = '/home/ubuntu/.ssh/config'
new_sshcfg = '/home/ubuntu/.ssh/NEWconfig'
IdentLine = '\tIdentityFile ~/.ssh/DBA-AWS00-Self-Signed.pem\n'

f1 = open(allnodes, 'r')
f2 = open(new_sshcfg, 'w')

for node in f1:
	HostLine = 'Host {0}'.format(node)
	f2.write(HostLine)
	f2.write(IdentLine)

f1.close()
f2.close()

os.rename(sshcfg, sshcfg + time.strftime('%Y%m%d_%H%M'))
os.rename(new_sshcfg, sshcfg)

print("... .ssh/config recreated")
