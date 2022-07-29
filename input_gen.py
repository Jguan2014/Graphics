import random
import matplotlib.pyplot as plt 
import numpy as np 
import math 

write_output = 1
size = 480

nrows = size
ncols = size 
x_width = 8
y_width = 8
num_xy = 6  #number of x-y pairs per line segment
linewidth = 2

rgb_bitwidth = 8; 

end_points = [[2,2],[26,118],[26,118],[26,118],[26,118],[48,2],[48,2],[66,118]]


def int2bi(data,bit_width):
	bi = str(bin(data))
	bi_chop = bi[2:]
	if(bit_width - len(bi_chop) > 0):
		new_bi = (bit_width - len(bi_chop))* '0' + str(bi_chop)	
	else:
		new_bi = bi_chop
	return new_bi 
		
def norm(data, max_val, width):
	div = (data / max_val) * 100
	return int2bi(data,width)
		

def gen_circle(raster_rgb,center,radius):
	angles = np.linspace(0, 6.28, num= int(radius*4))
	for a in angles:
		x = int(center[0] + radius*math.cos(a)) 
		y = int(center[1] + radius*math.sin(a)) 
		raster_rgb[y,x,0] = 250
		raster_rgb[y,x+1,0] = 250
		raster_rgb[y,x-1,0] = 250
		raster_rgb[y+1,x,0] = 250
		raster_rgb[y-1,x,0] = 250
		raster_rgb[y,x,1] = 20
		raster_rgb[y,x,2] = 20
		if x > center[0] and y>center[1]:
			raster_rgb[y-1,x-1,0] = 250
		if x < center[0] and y>center[1]:
			raster_rgb[y+1,x-1,0] = 250
		if x < center[0] and y<center[1]: 
			raster_rgb[y+1,x+1,0] = 250
		if x > center[0] and y<center[1]: 
			raster_rgb[y-1,x+1,0] = 250
	return raster_rgb 

def anti_aliasing(nrows,ncols,stroke_rgb,raster_rgb,vth):
        data = stroke_rgb.copy()  
        data1 = stroke_rgb.copy()  
	for i in range(nrows):
                for j in range(ncols):
                        avg1 = data[i][j]
                        count1 = 1
                        for k in [-1,1]:
                                for f in [1,-1]:
                                        row = i + k  #offset 
                                        col = f + j
                                        if i>0 and i <nrows-1 and j>0 and j<ncols-1: #boundary checking 
                                                #Edge detection: when a black pixel neighbours a white pixel  
                                                if data[i][j] == 0 and ((data[i][j+1] > vth or data[i][j-1] > vth) or  (data[i+1][j] > vth or data[i-1][j] > vth)):
                                                        avg1 += data[row][col]
                                                        count1 = count1 +1
                        avg1 = avg1 / count1
                        data1[i][j] = 255 - avg1
        return data1

def anti_aliasing_sub_pixel(nrows,ncols,stroke_ss_rgb,raster_rgb,vth):
        data = stroke_ss_rgb.copy()  
        aa_data= raster_rgb.copy()  

        avg = 0 
 	row = 0
 	col = 0
	for i in range(1,nrows-1,2):
                for j in range(1,ncols-1,2):
                	avg = (stroke_ss_rgb[i][j] + stroke_ss_rgb[i][j+1] + stroke_ss_rgb[i+1][j] + stroke_ss_rgb[i+1][j+1])/4
        		if avg == 0:   
        			aa_data[row][col] = raster_rgb[row][col]
        		else:
        			aa_data[row][col] = avg 
        		col = col + 1
        	row = row + 1 
        	col = 0
        return aa_data


def anti_aliasing_3d(nrows,ncols,stroke_ss_rgb,raster_rgb,vth):
	 raster = raster_rgb.copy()
	 red_aa = anti_aliasing(nrows,ncols,stroke_ss_rgb[:,:,0],raster_rgb[:,:,0],vth)
	 grn_aa = anti_aliasing(nrows,ncols,stroke_ss_rgb[:,:,1],raster_rgb[:,:,1],vth)
	 blu_aa = anti_aliasing(nrows,ncols,stroke_ss_rgb[:,:,2],raster_rgb[:,:,2],vth)
	 raster[:,:,0] = red_aa
	 raster[:,:,1] = grn_aa
	 raster[:,:,2] = blu_aa
	 return raster 
	 
#generates x,y,r,g,b,a values 
def gen_xy_input(end_points,rgb_bitwidth):
	x_array = []
	y_array = []
	x_bi_array = []
	y_bi_array = []
	if write_output:
		fx = open("x_input.txt", "w")
		fy = open("y_input.txt", "w")
		frgb = open("rgb_input.txt", "w")
		fv = open("v_input.txt", "w")
	rgb_array = []
	v_array = []
	v = 1   #should be 3 bit?
	for i in range(0,len(end_points),2):
		r = 0
		g = random.randint(50,180)
		b = random.randint(50,180)

		start = end_points[i]
		end = end_points[i+1]
		
		x,y = start
		avgx,avgy= x,y 
		dx = 20
		dy = 20
		flag = [0,0]	
		while abs(dx) >2 or abs(dy)>2:
			cx, cy = 0,0
			dx = end[0] - avgx
			dy = end[1] - avgy
			if dx ==0:
				y = y + y/abs(y)
			elif dy ==0:
				x = x +x/abs(x)
			else:
				if abs(dx) >= abs(dy):
					if flag[0] < 6:  
						x = x + dx/abs(dx)
						flag[0] = flag[0]+1
					else:
						y = y + dy/abs(dy)
						flag[0] = 0
					cx = 1 
				elif abs(dy) > abs(dx): 
					if flag[1] < 6: 
						y = y + dy/abs(dy)
						flag[1] = flag[1] +1
					else:
						x = x + dx/abs(dx)
						flag[1] = 0
					cy = 1
			x_array.append(x)
			y_array.append(y)
			rgb_array.append([r, g, b])
			v_array.append(v)

			avgx = (avgx+x)/2
			avgy = (avgy+y)/2
			if write_output: 
				x_bi = int2bi(int(x),12)
				y_bi = int2bi(int(y),12)
				r_bi = int2bi(int(r),rgb_bitwidth) 
				g_bi = int2bi(int(g),rgb_bitwidth) 
				b_bi = int2bi(int(b),rgb_bitwidth) 
				v_bi = int2bi(int(v),1) 
				fx.write(x_bi+"\n")
				fy.write(y_bi+"\n")
				frgb.write(r_bi+g_bi+b_bi+"\n")
				fv.write(v_bi+"\n")

	if write_output:
		fx.close()
		fy.close()
		frgb.close()
		fv.close()
	return x_array,y_array,rgb_array,v_array

#generates r,g,b values 
def raster_input(size):
	#set the random seed so we all get the same matrix
	seed = np.random.RandomState(2021)
	#create a 48 X 48 checkerboard of random colours
	rgb_array = seed.randint(0,1,size=(size,size,3))
	return rgb_array
	
#plot raster buffer output 
def plot_pixel(rgb_array):
	pixel_plot = plt.figure()
	plt.imshow(rgb_array,interpolation = 'nearest', origin = 'lower')
	plt.show()

#plot line segment
def plot_xy(x_arr,y_arr,num_xy):
	fig,xy_plot = plt.subplots()
	for i in range(len(x_arr)/num_xy):
		xy_plot.plot(x_arr[num_xy*i:num_xy*i-1],y_arr[num_xy*i:num_xy*i-1],linewidth = 4)
	#xy_plot.plot(x_arr[0:2],y_arr[0:2],linewidth = 4)
	plt.show()


def write_pixel(sum_rgb1,nrows,ncols):
	frgb = open("rgb_input.txt","w") 
	for x in range(nrows):
		for y in range(ncols):
			rgb = ''
			r= int2bi(sum_rgb1[x,y,0],8)
			g= int2bi(sum_rgb1[x,y,1],8)
			b= int2bi(sum_rgb1[x,y,2],8)
			rgb = str(r)+str(g)+str(b)
			frgb.write(rgb+"\n")						
	frgb.close()

def plot_output(raster):
	f_out = open("output_rgb_by4.txt","r")
	rgbs = f_out.readlines()
	x = 0
	y = 0
	for rgb in rgbs:
		raster[x,y,0] = int(rgb[0:7],2)
		raster[x,y,1] = int(rgb[8:15],2)
		raster[x,y,2] = int(rgb[16:23],2)
		y= y+1 
		if y == ncols:
			y = 0
			x = x + 1
	return raster 

def cap(sum_rgb1,nrows,ncols):
	for x in range(nrows):
		for y in range(ncols):
			if sum_rgb1[x,y,0] > 255:	
				sum_rgb1[x,y,0] = 255
			if sum_rgb1[x,y,1] > 255:	
				sum_rgb1[x,y,1] = 255
			if sum_rgb1[x,y,2] > 255:	
				sum_rgb1[x,y,2] =  255
	return sum_rgb1



#given a sub_pixel factor of 2, scale up the stroke array 
def write_to_stroke_ss_buffer(x_input,y_input,rgb_input,stroke_rgb,stroke_ss_rgb):
	for i in range(len(x_input)):
		x = x_input[i]
		y = y_input[i]
		r,g,b = rgb_input[i]
		for delta in [-1,0,1]:
			stroke_ss_rgb[y,x+delta,0] = r
			stroke_ss_rgb[y,x+delta,1] = g
			stroke_ss_rgb[y,x+delta,2] = b

	return stroke_ss_rgb

raster_rgb = raster_input(size)
stroke_rgb = raster_rgb.copy()
merged_rgb = raster_rgb.copy()
rgb_aa = raster_rgb.copy()

seed = np.random.RandomState(2021)
stroke_rgb_ss_array = seed.randint(0,1,size=(size,size,3))

#given end point pairs, generate x y r g b values 
x_arr, y_arr, rgb_arr,v_arr= gen_xy_input(end_points,rgb_bitwidth)

#given x y r g b, write to stroke buffer (super sampling stroke buffer)
rgb_ss_array = write_to_stroke_ss_buffer(x_arr,y_arr,rgb_arr,stroke_rgb,stroke_rgb_ss_array)

raster_cir = gen_circle(raster_rgb,[96,60],20)

merged_rgb = raster_rgb + rgb_ss_array + raster_cir


#rgb_aa = anti_aliasing_3d(nrows*2,ncols*2,stroke_rgb_ss_array,raster_rgb,1)
rgb_aa = anti_aliasing_3d(nrows,ncols,merged_rgb,raster_rgb,1)
plot_pixel(rgb_aa) 

#write_pixel(sum_rgb1,nrows,ncols)
