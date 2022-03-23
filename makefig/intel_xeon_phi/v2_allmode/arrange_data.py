#!/usr/bin/env python

import sys

def arrange_data(filename):
	f = open(filename, 'r')
	f_out = open(filename + '_arranged.csv', 'w')

	s = ''
	line = f.readline()
	while line:
		if 'mcdram_interleave_num' in line:
			mcdram_il = int(line.replace('mcdram_interleave_num: ','').strip())
		elif 'dram_interleave_num' in line:
			dram_il = int(line.replace('dram_interleave_num: ','').strip())

		if 'MCDRAM START' in line:
			il = mcdram_il
			il_list = [''] * il
		elif 'DRAM START' in line:
			il = dram_il
			il_list = [''] * il

		if 'mem numa' in line:
			mem_s = 'mem' + line.replace('mem numa: ','').strip()
			#s += mem_s + '\n'

		if 'core: 67' in line:
			flag = 'true'
		else:
			flag = 'false'
		if 'core: ' in line:
			core = line.replace('core: ','').strip()
			for i in range(0, il):
				while not 'Interleaving num: ' in line:
					line = f.readline()
				if i != int(line.replace('Interleaving num: ','').strip()):
					print('wrong format')
					sys.exit()
				while not 'Repeated test: Latency (ns): ' in line:
					line = f.readline()
				latency = line.replace('Repeated test: Latency (ns): ', '').strip()
				il_list[i] += core + ', ' + latency + '\n'

			if flag == 'true':
				for i in range(0, il):
					s += mem_s + '_interleaving'+str(i)+'\n'
					s += il_list[i]
					il_list[i] = ''
				
		line = f.readline()

	f.close()
	f_out.write(s)
	f_out.close()


if __name__ == '__main__':
	#argc = len(sys.argv)
	arrange_data(sys.argv[1])



