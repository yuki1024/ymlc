#!/usr/bin/env python

import sys

def arrange_data(filename):
	f = open(filename, 'r')
	f_out = open(filename + '_arranged.csv', 'w')

	s = ''
	line = f.readline()
	while line:
		if 'mem numa: ' in line:
			mem = line.replace('mem numa: ','').strip()
		if 'core: ' in line:
			core = line.replace('core: ','').strip()
		if 'Repeated test: Latency (ns): ' in line:
			lat = line.replace('Repeated test: Latency (ns): ','').strip()
			s += mem + ',' + core + ',' + lat + '\n'
		line = f.readline()

	f.close()
	f_out.write(s)
	f_out.close()

if __name__ == '__main__':
	#argc = len(sys.argv)
	arrange_data(sys.argv[1])



