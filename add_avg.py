#!/usr/bin/env python

import sys
import subprocess
import json

f_in = open('result_snalt0.json', 'r')
j_in = json.load(f_in)

avg_l = []
for v in list(j_in.values())[0]:
	avg_l.append(0)
#print(avg_l)

count = 0
for mn_k, mn_v in j_in.items():
	for k, v in mn_v.items():
		avg_l[int(k)] += float(v['latency'])
	count += 1
#print(avg_l)

for i,v in enumerate(avg_l):
	avg_l[i] /= 4
#print(avg_l)

j_in['avg'] = {}
for i,v in enumerate(avg_l):
	j_in['avg'][i] = {}
	j_in['avg'][i]['position'] = {}
	j_in['avg'][i]['position']['x'] = 0
	j_in['avg'][i]['position']['y'] = 0
	j_in['avg'][i]['latency'] = str(avg_l[i])
#print(j_in)

f_out = open('temp_out.json', 'x')
json.dump(j_in, f_out, indent='\t')



