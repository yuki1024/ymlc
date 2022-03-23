#!/usr/bin/env python

import sys
import subprocess
import numpy as np

#--------------------------------------------------------
cmd = 'rm -f result*'

cmd = 'hostname | tee -a result'
subprocess.call(cmd, shell=True)

#--------------------------------------------------------
#main

for mem in range(8):
	for core in range(128):
		cmd = 'echo "mem numa: ' + str(mem) + '" | tee -a result'
		subprocess.call(cmd, shell=True)
		cmd = 'echo "core: ' + str(core) + '" | tee -a result'
		subprocess.call(cmd, shell=True)
		#cmd = 'rm -f ymlc_exe'
		#subprocess.call(cmd, shell=True)
		#cmd = 'gcc -O0 -DINTERLEAVE_NUM=' + str(dram_interleave_num) + ' ymlc.c -o ymlc_exe'
		#subprocess.call(cmd, shell=True)
		cmd = 'numactl --physcpubind=' + str(core) + ' --membind=' + str(mem) + ' ./ymlc_exe | tee -a result'
		subprocess.call(cmd, shell=True)

subprocess.call(cmd, shell=True)

#--------------------------------------------------------
print('Finished')



