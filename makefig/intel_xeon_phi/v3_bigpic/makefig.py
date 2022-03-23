#!/usr/bin/env python

import math
import sys
from PIL import Image, ImageDraw, ImageFont

#global constant
w_base = 1600 #size of an exp window
h_base = 1400
max_row_num = 3
max_col_num = 4
max_width = w_base * max_col_num
max_height = h_base * max_row_num

#global
img = Image.new('RGB', (max_width, max_height), (255, 255, 255))
draw = ImageDraw.Draw(img)

#----------------------------------------------------------------------
#----------------------------------------------------------------------

def makefig_one(ch, coord, result, result_s, topo, topo_idxnum):
	draw.rectangle((coord[0],coord[1],coord[2]-1,coord[3]-1), fill=(255, 255, 255), outline=(0, 0, 0), width=1)

	#w = w_base/20*1.5 #size of a core
	#h = h_base/20*1.5
	w = 120 #size of a core
	h = 120

	#title
	font = ImageFont.truetype(font='DejaVuSans.ttf',size=55)
	draw.text((coord[0]+w*4, coord[1]+h/2), result_s[ch], fill=(0, 0, 0), font=font)

	margin_top = h_base/7
	margin_left = w_base/20

	minmax_list = []
	for i in range(len(result[ch])):
		if result[ch][i] > 0:
			minmax_list.append(result[ch][i])

	cmax = max(minmax_list)
	cmin = min(minmax_list)

	#min,max,delta
	font = ImageFont.truetype(font='DejaVuSans.ttf',size=55)
	draw.text((coord[0]+w*2, coord[1]+h*9.2), 'min = '+str(math.floor(cmax*10)/10)+' (ns)', fill=(0, 0, 0), font=font)
	draw.text((coord[0]+w*2, coord[1]+h*10.2), 'max = '+str(math.floor(cmin*10)/10)+' (ns)', fill=(0, 0, 0), font=font)
	draw.text((coord[0]+w*7, coord[1]+h*9.6), 'delta = '+str(math.floor((cmax-cmin)*10)/10)+' (ns)', fill=(0, 0, 0), font=font)

	for i in topo:
		pc = i[0] #physical ture core num

		c1 = coord[0] + margin_left + i[5]*w
		c2 = coord[1] + margin_top + i[4]*h
		c3 = coord[0] + margin_left + i[5]*w + w
		c4 = coord[1] + margin_top + i[4]*h + h

		if i[2] >= 0:
			color = coloring(result[ch][pc],cmin,cmax)
		elif i[2] == -1:
			color = (120,120,120)
		elif i[2] == -2:
			color = (120,120,120)
		else:
			print('format error')
			sys.exit()
		draw.rectangle((c1,c2,c3,c4), fill=color, outline=(0, 0, 0), width=1)

		#processor num
		if i[topo_idxnum] >= 0:
			font = ImageFont.truetype(font='DejaVuSans.ttf',size=40)
			draw.text((c1+w/3,c2+h/15,c3+w/4,c4+h/15), str(i[topo_idxnum]), fill=(0,0,0), font=font)

		#latency num
		if i[topo_idxnum] >= 0:
			font = ImageFont.truetype(font='DejaVuSans.ttf',size=32)
			ltc_s = '{0:.1f}'.format(result[ch][pc])
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
	f_setting = open('topology_snedo01', 'r')

	line = f_setting.readline()
	while '#' in line:
		line = f_setting.readline()

	topo = []
	for i in range(0,76):
		if i != int((line.split(','))[0]):
			print('format error')
			sys.exit()
		temp_list = map(int, line.strip().split(','))
		#(true core, snc4 processor num, core id, quadrant processor num, row, col)
		#-1: silent missing
		#-2: missing
		topo.append(temp_list)
		line = f_setting.readline()
	#print(topo)

	#----------------------------------------------------------------------
	#vertical topo
	v_topo = []
	temp0 = []
	temp1 = []
	temp2 = []
	temp3 = []
	temp4 = []
	temp5 = []
	for i in range(len(topo)):
		temp0.append(topo[i][0])
		temp1.append(topo[i][1])
		temp2.append(topo[i][2])
		temp3.append(topo[i][3])
		temp4.append(topo[i][4])
		temp5.append(topo[i][5])
	v_topo.append(temp0)
	v_topo.append(temp1)
	v_topo.append(temp2)
	v_topo.append(temp3)
	v_topo.append(temp4)
	v_topo.append(temp5)
	#print(v_topo)

	#----------------------------------------------------------------------
	f = open(hname, 'r')

	topo_idxnum = 1
	if 'snc4' in hname:
		topo_idxnum = 1
	elif ('quadrant' in hname) or ('all2all' in hname):
		topo_idxnum = 3
	else:
		print('format error')
		sys.exit()

	result = []
	result_s = []

	line = f.readline()
	while line:
		ch = [-1]*76 #memory channel
		if 'mem' in line:
			ch_s = line.strip()

			line = f.readline()

			for i in range(67): #all active core num = 76-8-1 = 67core
				proc_num = int(line.split(', ')[0])
				exp_num = float((line.split(', ')[1]).strip())

				idx = (v_topo[topo_idxnum]).index(proc_num)
				ch[idx] =  exp_num

				line = f.readline()

			result.append(ch)
			result_s.append(ch_s)

	#print(result_s)

	#----------------------------------------------------------------------

	if (max_width%4 != 0) or (max_height%2 != 0):
		print("error")
		sys.exit()
	w = w_base
	h = h_base

	all_coord = (
		(0,0,w,h),
		(w,0,w*2,h),
		(w*2,0,w*3,h),
		(w*3,0,w*4,h),
		(0,h,w,h*2),
		(w,h,w*2,h*2),
		(w*2,h,w*3,h*2),
		(w*3,h,w*4,h*2),
		(0,h*2,w,h*3),
		(w,h*2,w*2,h*3),
		(w*2,h*2,w*3,h*3),
		(w*3,h*2,w*4,h*3),
	)

	for i in range(0, len(result)):
		makefig_one(i, all_coord[i], result, result_s, topo, topo_idxnum)

	img.save(hname.replace('_arranged.csv','').replace('result_snedo01_','')+'_fig.png')

if __name__ == '__main__':
	makefig_all(sys.argv[1])



