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
cmd = 'sudo wrmsr -a 0x1a4 07'
#cmd = 'sudo wrmsr -a 0x1a4 0xf'
#cmd = 'sudo wrmsr -a 0x1a4 0'
subprocess.call(cmd, shell=True)
cmd = 'sudo rdmsr 0x1a4'
subprocess.call(cmd, shell=True)

#--------------------------------------
#main

count_list = []
#for i in range(7,23,1):
#	count_list.append(2**i)
#count_list = map(lambda x: int(np.round(2**x)), np.arange(7.0, 23.1, 0.25))
#print(count_list)
#print(len(count_list))

cpu_list = range(0,68)
cpu_list.remove(14)
#print(cpu_list)
mem_list = range(0,8)

count = 1638400

cmd = 'rm -f result_mem*'
subprocess.call(cmd, shell=True)

#for i in count_list:
for mem in mem_list:
	for cpu in cpu_list:
		cmd = 'rm -f ymlc_exe'
		subprocess.call(cmd, shell=True)

		cmd = 'gcc -O0 -DCOUNT=' + str(count) + ' ymlc.c -o ymlc_exe'
		#cmd = 'gcc -O0 -DCOUNT=' + str(count) + ' -DRANDOM ymlc.c -o ymlc_exe'
		subprocess.call(cmd, shell=True)

		#for plot
		#for j in range(20):
		#	cmd = 'numactl --physcpubind=3 ./ymlc_exe'
		#	subprocess.call(cmd, shell=True)

		#for graph
		#cmd = 'numactl --physcpubind=3 ./ymlc_exe'
		#cmd = 'echo "cpu,mem=' + str(cpu) + ',' + str(mem) + '" >> result'
		cmd = 'echo "cpu=' + str(cpu) + '" >> result_mem' + str(mem)
		subprocess.call(cmd, shell=True)
		cmd = 'numactl --physcpubind=' + str(cpu) + ' --membind=' + str(mem) + ' ./ymlc_exe | tee -a result_mem' + str(mem)
		subprocess.call(cmd, shell=True)

#--------------------------------------
#hw prefetch on
cmd = 'sudo wrmsr -a 0x1a4 0'
subprocess.call(cmd, shell=True)
cmd = 'sudo rdmsr 0x1a4'
subprocess.call(cmd, shell=True)




