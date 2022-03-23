#!/usr/bin/env python

import sys

def arrange_data(filename):
	f = open(filename, 'r')
	f_out = open(filename + '_arranged', 'w')

	s = ''
	line = f.readline()
	while line:
		if 'processor\t: ' in line:
			processor = line.replace('processor\t: ','').strip()
		else:
			line = f.readline()
			continue
		for i in range(11):
			line = f.readline()
		if 'core id\t\t: ' in line:
			coreid = line.replace('core id\t\t: ', '').strip()
		else:
			print('wrong format')
			sys.exit()
		s += processor + ',' + coreid + '\n'

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



