#!/usr/bin/env python

import sys
import subprocess
#import numpy as np
import json

#--------------------------------------------------------

cmd = 'rm -f ymlc_exe result.json'
subprocess.call(cmd, shell=True)
cmd = 'gcc -O0 ymlc.c -o ymlc_exe'
subprocess.call(cmd, shell=True)

#--------------------------------------------------------

cmd = 'numactl -H'
out = subprocess.run(cmd, shell=True, encoding='utf-8', stdout=subprocess.PIPE)

cpus_s = []
mems_s = []

temp_list = out.stdout.split('\n')
for line in temp_list:
	if 'cpus: ' in line:
		cpus_s.extend((line.split('cpus: ')[1]).split(' '))
	if 'size: ' in line:
		mems_s.append((line.split(' size: ')[0]).replace('node ',''))

cpus = [int(s) for s in cpus_s]
mems = [int(s) for s in mems_s]

#--------------------------------------------------------

result = {}

for mem in mems:
	mem_s = 'mem_node_' + str(mem)
	result[mem_s] = {}

	for core in cpus:
		result[mem_s][str(core)] = {}
		result[mem_s][str(core)]['position'] = {}
		result[mem_s][str(core)]['position']['x'] = 0
		result[mem_s][str(core)]['position']['y'] = 0
		
		cmd = 'numactl --physcpubind=' + str(core) + ' --membind=' + str(mem) + ' ./ymlc_exe'
		out = subprocess.run(cmd, shell=True, encoding='utf-8', stdout=subprocess.PIPE)
	
		temp_list = out.stdout.split('\n')
		for line in temp_list:
			if 'Repeated test: Latency (ns): ' in line:
				result[mem_s][str(core)]['latency'] = line.replace('Repeated test: Latency (ns): ', '')

#--------------------------------------------------------
# Add avg

avg_l = []
for v in list(result.values())[0]:
	avg_l.append(0)
#print(avg_l)

count = 0
for mn_k, mn_v in result.items():
	for k, v in mn_v.items():
		avg_l[int(k)] += float(v['latency'])
	count += 1
#print(avg_l)

for i,v in enumerate(avg_l):
	avg_l[i] /= count
#print(avg_l)

result['avg'] = {}
for i,v in enumerate(avg_l):
	result['avg'][i] = {}
	result['avg'][i]['position'] = {}
	result['avg'][i]['position']['x'] = 0
	result['avg'][i]['position']['y'] = 0
	result['avg'][i]['latency'] = str(avg_l[i])
#print(result)

f = open('result.json', 'x')
json.dump(result, f, indent='\t')

#--------------------------------------------------------






