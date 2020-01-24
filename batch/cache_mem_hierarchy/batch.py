#!/usr/bin/env python

import sys
import subprocess
import numpy as np

#sudo check
#cmd = 'sudo ls /root/'
#subprocess.call(cmd, shell=True)

#clean
cmd = 'rm -f ymlc_exe'
subprocess.call(cmd, shell=True)

#hw prefetch off
#cmd = 'sudo wrmsr -a 0x1a4 07'
#cmd = 'sudo wrmsr -a 0x1a4 0xf'
cmd = 'sudo wrmsr -a 0x1a4 0'
subprocess.call(cmd, shell=True)
cmd = 'sudo rdmsr 0x1a4'
subprocess.call(cmd, shell=True)

#--------------------------------------
#main

count_list = []
#for i in range(7,23,1):
#	count_list.append(2**i)
count_list = map(lambda x: int(np.round(2**x)), np.arange(7.0, 23.1, 0.25))
#print(count_list)
#print(len(count_list))

for i in count_list:
	cmd = 'rm -f ymlc_exe'
	subprocess.call(cmd, shell=True)

	cmd = 'gcc -O0 -DCOUNT=' + str(i) + ' ymlc.c -o ymlc_exe'
	#cmd = 'gcc -O0 -DCOUNT=' + str(i) + ' -DRANDOM ymlc.c -o ymlc_exe'
	subprocess.call(cmd, shell=True)

	#for plot
	#for j in range(20):
	#	cmd = 'numactl --physcpubind=3 ./ymlc_exe'
	#	subprocess.call(cmd, shell=True)

	#for graph
	#cmd = 'numactl --physcpubind=3 ./ymlc_exe'
	cmd = 'numactl --physcpubind=0 --membind=4 ./ymlc_exe'
	subprocess.call(cmd, shell=True)

#--------------------------------------
#hw prefetch on
cmd = 'sudo wrmsr -a 0x1a4 0'
subprocess.call(cmd, shell=True)
cmd = 'sudo rdmsr 0x1a4'
subprocess.call(cmd, shell=True)




