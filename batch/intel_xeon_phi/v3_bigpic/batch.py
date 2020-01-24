#!/usr/bin/env python

import sys
import subprocess
import numpy as np

#--------------------------------------------------------
#sudo check
#cmd = 'sudo ls /root/'
#subprocess.call(cmd, shell=True)

#--------------------------------------------------------
#set machine profile
machine_name = 'mill0' #modified by hand

core_list = range(0,71)
#snedo01 Flat/SNC4
if machine_name == 'snedo01':
	core_list.remove(14) #missing core num
	mcdram_mem_numa_list = range(4,8)
	dram_mem_numa_list = range(0,4)
	mcdram_interleave_num = 2
	dram_interleave_num = 1
#snedo02 Flat/Quadrant
elif machine_name == 'snedo02':
	core_list.remove(60) #missing core num
	mcdram_mem_numa_list = [1]
	dram_mem_numa_list = [0]
	mcdram_interleave_num = 8
	dram_interleave_num = 2
#snedo03 Flat/All2All
elif machine_name == 'snedo03':
	core_list.remove(58) #missing core num
	mcdram_mem_numa_list = [1]
	dram_mem_numa_list = [0]
	mcdram_interleave_num = 8
	dram_interleave_num = 2
#mill0 Flat/SNC4
elif machine_name == 'mill0':
	mcdram_mem_numa_list = range(4,8)
	dram_mem_numa_list = range(0,4)
	mcdram_interleave_num = 2
	dram_interleave_num = 1
else:
	print('Error: unknown machine profile')
	sys.exit()

#--------------------------------------------------------
cmd = 'rm -f result*'

cmd = 'hostname | tee -a result'
subprocess.call(cmd, shell=True)
cmd = 'sudo hwloc-dump-hwdata | egrep "Cluster|Mode" | tee -a result'
subprocess.call(cmd, shell=True)

cmd = 'echo "core_list: ' + str(core_list) + '" | tee -a result'
subprocess.call(cmd, shell=True)
cmd = 'echo "mcdram_mem_numa_list: ' + str(mcdram_mem_numa_list) + '" | tee -a result'
subprocess.call(cmd, shell=True)
cmd = 'echo "dram_mem_numa_list: ' + str(dram_mem_numa_list) + '" | tee -a result'
subprocess.call(cmd, shell=True)
cmd = 'echo "mcdram_interleave_num: ' + str(mcdram_interleave_num) + '" | tee -a result'
subprocess.call(cmd, shell=True)
cmd = 'echo "dram_interleave_num: ' + str(dram_interleave_num) + '" | tee -a result'
subprocess.call(cmd, shell=True)

cmd = 'echo "----------------------------------------------" | tee -a result'
subprocess.call(cmd, shell=True)

#hw prefetch off
cmd = 'sudo wrmsr -a 0x1a4 07'
#cmd = 'sudo wrmsr -a 0x1a4 0xf'
#cmd = 'sudo wrmsr -a 0x1a4 0'
subprocess.call(cmd, shell=True)
cmd = 'sudo rdmsr 0x1a4'
subprocess.call(cmd, shell=True)

#--------------------------------------------------------
#main

cmd = 'echo "MCDRAM START" | tee -a result'
subprocess.call(cmd, shell=True)
for mem in mcdram_mem_numa_list:
	cmd = 'echo "mem numa: ' + str(mem) + '" | tee -a result'
	subprocess.call(cmd, shell=True)
	for core in core_list:
		cmd = 'echo "core: ' + str(core) + '" | tee -a result'
		subprocess.call(cmd, shell=True)
		cmd = 'rm -f ymlc_exe'
		subprocess.call(cmd, shell=True)
		cmd = 'gcc -O0 -DINTERLEAVE_NUM=' + str(mcdram_interleave_num) + ' ymlc.c -o ymlc_exe'
		subprocess.call(cmd, shell=True)
		cmd = 'numactl --physcpubind=' + str(core) + ' --membind=' + str(mem) + ' ./ymlc_exe | tee -a result'
		subprocess.call(cmd, shell=True)
cmd = 'echo "MCDRAM END" | tee -a result'
subprocess.call(cmd, shell=True)

cmd = 'echo "DRAM START" | tee -a result'
subprocess.call(cmd, shell=True)
for mem in dram_mem_numa_list:
	cmd = 'echo "mem numa: ' + str(mem) + '" | tee -a result'
	subprocess.call(cmd, shell=True)
	for core in core_list:
		cmd = 'echo "core: ' + str(core) + '" | tee -a result'
		subprocess.call(cmd, shell=True)
		cmd = 'rm -f ymlc_exe'
		subprocess.call(cmd, shell=True)
		cmd = 'gcc -O0 -DINTERLEAVE_NUM=' + str(dram_interleave_num) + ' ymlc.c -o ymlc_exe'
		subprocess.call(cmd, shell=True)
		cmd = 'numactl --physcpubind=' + str(core) + ' --membind=' + str(mem) + ' ./ymlc_exe | tee -a result'
		subprocess.call(cmd, shell=True)
cmd = 'echo "DRAM END" | tee -a result'
subprocess.call(cmd, shell=True)

#--------------------------------------------------------
#hw prefetch on
cmd = 'sudo wrmsr -a 0x1a4 0'
subprocess.call(cmd, shell=True)
cmd = 'sudo rdmsr 0x1a4'
subprocess.call(cmd, shell=True)

#--------------------------------------------------------
print('Finished')



