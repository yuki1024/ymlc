#!/usr/bin/env python

import sys

def arrange_data(filename):
	f = open(filename, 'r')
	f_out = open(filename + '_arranged.csv', 'w')

	s = ''
	line = f.readline()
	while line:
		if 'Total buffer size: ' in line:
			bufsize = line.replace('Total buffer size: ', '').replace('Byte', '').strip()
		else:
			line = f.readline()
			continue
		for i in range(7):
			line = f.readline()
		if 'Repeated test: Latency (ns): ' in line:
			latency = line.replace('Repeated test: Latency (ns): ', '').strip()
		else:
			print('wrong format')
			sys.exit()
		s += bufsize + ', ' + latency + '\n'

		line = f.readline()

	f.close()
	f_out.write(s)
	f_out.close()


if __name__ == '__main__':
	#argc = len(sys.argv)
	arrange_data(sys.argv[1])
	#if (sys.argv[1] == 'plot'):
	#	arrange_data_for_plot(sys.argv[2])
	#if (sys.argv[1] == 'graph'):
	#	arrange_data_for_plot(sys.argv[2])



