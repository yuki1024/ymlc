#!/usr/bin/env python

import sys
import pandas

#Notice!!!! This script is under construction. Does not work!!!!

def arrange_data(filename):

	df = pandas.read_csv(filename, header=None)

	print(df[df[:][1] == 61].iloc[0,0])
	df[df[:][1] == 61][1] = 5
	print(df[df[:][1] == 61][1])

	for i in list(range(0,18)) + list(range(36,54)):
		if i%4 >= 2:
			continue
		if (df[:][1] == i).any() & (df[:][1] == i+18).any():
			#temp = df[df[:][1]==i].iloc[0,0]
			#df[df[:][1]==i].iloc[0,0] = df[df[:][1]==i+18].iloc[0,0]
			#df[df[:][1]==i+18].iloc[0,0] = temp
			temp = df[df[:][1]==i].iloc[0,0]
			#df[df[:][1]==i][0] = df[df[:][1]==i+18].iloc[0,0]
			#df[df[:][1]==i+18][,0] = temp

	df.to_csv(filename + '_changed')


if __name__ == '__main__':
	#argc = len(sys.argv)
	arrange_data(sys.argv[1])
	#if (sys.argv[1] == 'plot'):
	#	arrange_data_for_plot(sys.argv[2])
	#if (sys.argv[1] == 'graph'):
	#	arrange_data_for_plot(sys.argv[2])



