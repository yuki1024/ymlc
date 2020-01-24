#!/usr/bin/env python

import sys

def csv2json(filename):
	f = open(filename, 'r')
	f_out = open(filename + '_json.js', 'w')

	s = ''
	s += 'export let json = \n{'
	line = f.readline()
	while line:
		if 'mem' in line:
			s += '"' + line.strip() + '": {\n'

			line = f.readline()
			while (line) and (not 'mem' in line):
				simple_line = line.strip().split(', ')
				s += '"' + simple_line[0] + '": ' + simple_line[1] + ',\n'

				line = f.readline()

			s += '},\n'

	s += '};'

	f.close()
	f_out.write(s)
	f_out.close()

if __name__ == '__main__':
	#argc = len(sys.argv)
	csv2json(sys.argv[1])



