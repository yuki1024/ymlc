#!/usr/bin/env python

import math
import sys
from PIL import Image, ImageDraw, ImageFont

#global constant
w_base = 1600 #size of an exp window
h_base = 1600
#w_base = 400 #size of an exp window
#h_base = 400
max_row_num = 4
max_col_num = 4
max_width = w_base * max_col_num
max_height = h_base * max_row_num

#global
img = Image.new('RGB', (max_width, max_height), (255, 255, 255))
draw = ImageDraw.Draw(img)

#----------------------------------------------------------------------
#----------------------------------------------------------------------

def makefig_one(ch, coord, result):
	draw.rectangle((coord[0],coord[1],coord[2]-1,coord[3]-1), fill=(255, 255, 255), outline=(0, 0, 0), width=1)

	mem = int(math.floor(ch/2))
	if ch%2 == 0:
		socket = 0
		core_list = range(0,64)
	elif ch%2 == 1:
		socket = 1
		core_list = range(64,128)

	#w = w_base/20*1.5 #size of a core
	#h = h_base/20*1.5
	w = 120 #size of a core
	h = 120

	#title
	font = ImageFont.truetype(font='DejaVuSans.ttf',size=55)
	draw.text((coord[0]+w*5, coord[1]+h/2), 'mem'+str(mem)+'_socket'+str(socket), fill=(0, 0, 0), font=font)

	margin_top = h_base/9
	margin_left = w_base/6

	minmax_list = []
	for i in core_list:
		if result[mem][i] > 0:
			minmax_list.append(result[mem][i])

	cmax = max(minmax_list)
	cmin = min(minmax_list)

	#min,max,delta
	font = ImageFont.truetype(font='DejaVuSans.ttf',size=55)
	draw.text((coord[0]+w*2, coord[1]+h*11.2), 'min = '+str(math.floor(cmax*10)/10)+' (ns)', fill=(0, 0, 0), font=font)
	draw.text((coord[0]+w*2, coord[1]+h*12.2), 'max = '+str(math.floor(cmin*10)/10)+' (ns)', fill=(0, 0, 0), font=font)
	draw.text((coord[0]+w*7, coord[1]+h*11.6), 'delta = '+str(math.floor((cmax-cmin)*10)/10)+' (ns)', fill=(0, 0, 0), font=font)

	grid = []
	count = 0
	for soc in range(2):
		for numa in range(4):
			if numa == 0:
				numa_x = 0
				numa_y = 0
			elif numa == 1:
				numa_x = 5
				numa_y = 0
			elif numa == 2:
				numa_x = 0
				numa_y = 5
			elif numa == 3:
				numa_x = 5
				numa_y = 5

			for row in range(4):
				for col in range(4):
					grid.append([])
					grid[count].append(numa_y + row)
					grid[count].append(numa_x + col)
					count += 1

	if len(grid) != 128:
		print('grid len error')
		sys.exit()

	for core in core_list:

		c1 = coord[0] + margin_left + grid[core][1]*w
		c2 = coord[1] + margin_top + grid[core][0]*h
		c3 = coord[0] + margin_left + grid[core][1]*w + w
		c4 = coord[1] + margin_top + grid[core][0]*h + h

		color = coloring(result[mem][core],cmin,cmax)

		draw.rectangle((c1,c2,c3,c4), fill=color, outline=(0, 0, 0), width=1)

		#processor num
		font = ImageFont.truetype(font='DejaVuSans.ttf',size=40)
		draw.text((c1+w/3,c2+h/15,c3+w/4,c4+h/15), str(core), fill=(0,0,0), font=font)

		#latency num
		font = ImageFont.truetype(font='DejaVuSans.ttf',size=32)
		ltc_s = '{0:.1f}'.format(result[mem][core])
		draw.text((c1+w/7,c2+h/1.8,c3+w/8,c4+h/1.8), ltc_s, fill=(0, 0, 0), font=font)


#----------------------------------------------------------------------
def coloring(num, cmin, cmax):
	if (num < cmin) or (num > cmax):
		print("coloring error")
		sys.exit()

	crange = cmax - cmin
	red = int((float(255)*(num-cmin)/crange))
	green = int((float(255)*(cmax-num)/crange))

	return (red,green,255)


#----------------------------------------------------------------------
def makefig_all(hname):

	f = open(hname, 'r')

	result = []
	for i in range(8):
		result.append([])

	line = f.readline()
	while line:
		mem = int(line.split(',')[0])
		core = int(line.split(',')[1])
		lat = float(line.split(',')[2])

		result[mem].append(lat)
		if len(result[mem]) != core+1:
			print(core)
			print(mem)
			print('core num error')
			sys.exit()

		line = f.readline()

#----------------------------------------------------------------------

	if (max_width%4 != 0) or (max_height%2 != 0):
		print("max size error")
		sys.exit()
	w = w_base
	h = h_base

	all_coord = (
		(w*0,h*0,w*1,h*1),
		(w*1,h*0,w*2,h*1),
		(w*2,h*0,w*3,h*1),
		(w*3,h*0,w*4,h*1),
		(w*0,h*1,w*1,h*2),
		(w*1,h*1,w*2,h*2),
		(w*2,h*1,w*3,h*2),
		(w*3,h*1,w*4,h*2),
		(w*0,h*2,w*1,h*3),
		(w*1,h*2,w*2,h*3),
		(w*2,h*2,w*3,h*3),
		(w*3,h*2,w*4,h*3),
		(w*0,h*3,w*1,h*4),
		(w*1,h*3,w*2,h*4),
		(w*2,h*3,w*3,h*4),
		(w*3,h*3,w*4,h*4),
	)

	for i in range(0, len(all_coord)):
		makefig_one(i, all_coord[i], result)

	img.save(hname.replace('_arranged.csv','')+'_fig.png')

if __name__ == '__main__':
	makefig_all(sys.argv[1])



