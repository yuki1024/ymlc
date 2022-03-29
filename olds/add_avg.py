#!/usr/bin/env python

import sys
import subprocess
import json

f_in = open('result_snedo01.json', 'r')
j_in = json.load(f_in)

avg_d = {}
for v in list(j_in.values())[0]:
	avg_d[v] = 0
#print(avg_d)

count = 0
for mn_k, mn_v in j_in.items():
	for k, v in mn_v.items():
		avg_d[k] += float(v['latency'])
	count += 1
#print(avg_d)

for i,v in avg_d.items():
	avg_d[i] /= count
#print(avg_d)

j_in['avg'] = {}
for i,v in avg_d.items():
	j_in['avg'][i] = {}
	j_in['avg'][i]['position'] = {}
	j_in['avg'][i]['position']['x'] = 0
	j_in['avg'][i]['position']['y'] = 0
	j_in['avg'][i]['latency'] = str(avg_d[i])
#print(j_in)

f_out = open('result_snedo01_withavg.json', 'x')
json.dump(j_in, f_out, indent='\t')



