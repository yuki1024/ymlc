#!/usr/bin/env python

import sys
from PIL import Image, ImageDraw, ImageFont
import pandas

#constant
max_width = 1600
max_height = 800

#global
img = Image.new('RGB', (max_width, max_height), (255, 255, 255))
draw = ImageDraw.Draw(img)

def makefig_one(memnum, coord):
	#draw.rectangle(coord, fill=(255, 255, 255), outline=(0, 0, 0), width=1)
	draw.rectangle((coord[0],coord[1],coord[2]-1,coord[3]-1), fill=(255, 255, 255), outline=(0, 0, 0), width=1)

	win_w = coord[2] - coord[0]
	win_h = coord[3] - coord[1]
	w = win_w / 20
	h = win_h / 20

	font = ImageFont.truetype(font='DejaVuSans.ttf',size=20)
	draw.text((coord[0]+win_w/2-30, coord[1]+20), 'mem'+str(memnum), fill=(0, 0, 0), font=font)

	all_coord = []
	#for offset in ((50,70),(50,200),(200,70),(200,200)):
	#for offset in ((50,70),(200,70),(50,200),(200,200)):
	for offset in ((65,70),(65,160),(215,70),(215,160)):
		for i in range(3):
			for j in range(6):
				all_coord.append([offset[0]+w*j, offset[1]+h*i])
	#print(all_coord)

	df = pandas.read_csv('result_mem' + str(memnum) + '_arranged.csv', header=None)
	#print(df)
	#print(df.iloc[0,0])
	#print(df.iloc[:][1].min())
	#print(df.iloc[:][1].max())

	cmin = df.iloc[:][1].min()
	#cmin = 0.0
	cmax = df.iloc[:][1].max()

	count = 0
	gap = 0
	sgap = 0
	for i in all_coord:
		if count == 14:
			color = (0,256,0)
			gap += 1
			sgap += 1
			s = '14'
		#elif count in (40, 41, 60, 61):
		#elif count in (30, 31, 40, 41):
		#elif count in (50, 51, 60, 61):
		#elif count in (44, 45, 46, 47):
		#elif count in (44, 45, 60, 61):
		elif count in (40, 41, 54, 55):
			color = (128,128,128)
			gap += 1
			s = ''
		else:
			color = coloring(df.iloc[count-gap,1],cmin,cmax)
			s = str(count-gap+sgap)
		#draw.rectangle((coord[0]+i[0], coord[1]+i[1], coord[0]+i[0]+w, coord[1]+i[1]+h), fill=coloring(1.0,0.0,2.0), outline=(0, 0, 0), width=1)
		draw.rectangle((coord[0]+i[0], coord[1]+i[1], coord[0]+i[0]+w, coord[1]+i[1]+h), fill=color, outline=(0, 0, 0), width=1)

		font = ImageFont.truetype(font='DejaVuSans.ttf',size=10)
		#draw.text((coord[0]+i[0], coord[1]+i[1], coord[0]+i[0]+w, coord[1]+i[1]+h), str(count), fill=(0, 0, 0), font=font)
		#draw.text((coord[0]+i[0]+w/4, coord[1]+i[1]+h/4), s, fill=(0, 0, 0), font=font)

		font = ImageFont.truetype(font='DejaVuSans.ttf',size=8)
		draw.text((coord[0]+i[0]+w/6, coord[1]+i[1]+h/6), str(int(df.iloc[count-gap,1])), fill=(0, 0, 0), font=font)

		count += 1

	font = ImageFont.truetype(font='DejaVuSans.ttf',size=15)
	draw.text((coord[0]+100, coord[1]+250), 'min = ' + str(cmin) + ' (ns)', fill=(0, 0, 0), font=font)
	draw.text((coord[0]+100, coord[1]+270), 'max = ' + str(cmax) + ' (ns)', fill=(0, 0, 0), font=font)


def coloring(num, min_num, max_num):
	#RGB based
	#Blue one color based
	#Must: num,min_num,max_num: float
	if (num < min_num) or (num > max_num):
		print("error")
		sys.exit()

	#red
	#color = 255 - int((float(255)*(num-min_num)/(max_num-min_num)))
	#return (255,color,color)

	#blue
	color = int((float(255)*(num-min_num)/(max_num-min_num)))
	return (color,color,255)



def makefig_all():
	if (max_width%4 != 0) or (max_height%2 != 0):
		print("error")
		sys.exit()
	w = max_width/4
	h = max_height/2

	all_coord = (
		(0,0,w,h),
		(w,0,w*2,h),
		(0,h,w,h*2),
		(w,h,w*2,h*2),
		(w*2,0,w*3,h),
		(w*3,0,w*4,h),
		(w*2,h,w*3,h*2),
		(w*3,h,w*4,h*2)
	)

	for i in range(8):
		makefig_one(i, all_coord[i])

	img.save('fig.png')


if __name__ == '__main__':
	makefig_all()



