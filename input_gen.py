import random
import matplotlib.pyplot as plt 
import numpy as np 
import math 

write_output = 0
size = 100
nrows = 100
ncols = 100
x_width = 9
y_width = 9
num_xy = 30  #number of x-y pairs per line segment
linewidth = 2
slope = 1;
y_intercept = 10;

rgb_bitwidth = 8; 

num_seg = 2
def int2bi(data,bit_width):
	bi = bin(data)
	bi = bi[2:]
	if(bit_width - len(bi) > 0):
		bi = (bit_width - len(bi))* '0' + bi	
	return bi 
		
def norm(data, max_val, width):
	div = (data / max_val) * 100
	return int2bi(data,width)
		

def gen_circle(raster_rgb,center,radius):
	angles = np.linspace(0, 6.28, num= int(radius*3.14))
	for a in angles:
		x = int(center[0] + radius*math.cos(a)) 
		y = int(center[1] + radius*math.sin(a)) 
		raster_rgb[x,y,0] = 250
		raster_rgb[x,y,1] = 0
		raster_rgb[x,y,2] = 0
		if x > center[0] and y>center[1]:
			raster_rgb[x-1,y-1,0] = 250
		if x < center[0] and y>center[1]:
			raster_rgb[x+1,y-1,0] = 250
		if x < center[0] and y<center[1]: 
			raster_rgb[x+1,y+1,0] = 250
		if x > center[0] and y<center[1]: 
			raster_rgb[x-1,y+1,0] = 250
	return raster_rgb 

def anti_aliasing(nrows,ncols,data,th):
        data1 = data.copy()  
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
                                                if data[i][j] == 0 and ((data[i][j+1]>th or data[i][j-1]>th) or  (data[i+1][j]>th or data[i-1][j]>th)):
                                                        avg1 += data[row][col]
                                                        count1 = count1 +1;
                        avg1 = avg1 / count1
                        data1[i][j] = 255-avg1
        return data1


def anti_aliasing_3d(nrows,ncols,raster_rgb,vth):
	 raster = raster_rgb.copy()
	 red_aa = anti_aliasing(nrows,ncols,raster_rgb[:,:,0],vth)
	 grn_aa = anti_aliasing(nrows,ncols,raster_rgb[:,:,1],vth)
	 blu_aa = anti_aliasing(nrows,ncols,raster_rgb[:,:,2],vth)
	 raster[:,:,0] = red_aa
	 raster[:,:,1] = grn_aa
	 raster[:,:,2] = blu_aa
	 return raster 
	 
#generates x,y,r,g,b,a values 
def gen_xy_input(raster_rgb,num_xy,start,slope,y_intercept,num_seg,rgb_bitwidth,linewidth):
	x_array = []
	y_array = []
	x_bi_array = []
	y_bi_array = []
	fx = open("x_input.txt", "w")
	fy = open("y_input.txt", "w")
	frgb = open("rgb_input.txt", "w")
	fv = open("v_input.txt", "w")
	rgb_array = []
	v_array = []
	r = random.randint(0,255) #8-bit 
	g = random.randint(0,255)
	b = random.randint(0,255)
	v = 1
	x = start[0]
	for i in range (num_xy): #for each line segment, introduce some noises due to ADC
		y = slope*x+start[1]
		for m in  [0,1,2]:
			new_x = x
			new_y = y+m
			if new_x >= ncols: new_x = ncols-1
			if new_x < 0: new_x = 0
	        	if new_y >= nrows: new_y = nrows-1
			if new_y < 0: new_y = 0  
			raster_rgb[new_x,new_y,0] = r 
			raster_rgb[new_x,new_y,1] = g 
			raster_rgb[new_x,new_y,2] = b 
		if write_output: 
			x_bi = int2bi(int(x),8)
			y_bi = int2bi(int(y),8)
			r_bi = int2bi(int(r),rgb_bitwidth) 
			g_bi = int2bi(int(g),rgb_bitwidth) 
			b_bi = int2bi(int(b),rgb_bitwidth) 
			v_bi = int2bi(int(v),rgb_bitwidth) 
			fx.write(x_bi+"\n")
			fy.write(y_bi+"\n")
			frgb.write(str(r_bi)+str(g_bi) + str(b_bi) + str(v_bi)+"\n")
			fv.write(v_bi+"\n")
			x_array.append(x)
			y_array.append(y)
			rgb_array.append([r, g, b])
			v_array.append(v)
		x = x+1 
	fx.close()
	fy.close()
	frgb.close()
	fv.close()
	return x_array,y_array,rgb_array,v_array,raster_rgb

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



rgb_array_3d = raster_input(size)

x_arr, y_arr, rgb_arr,v_arr,raster_rgb = gen_xy_input(rgb_array_3d,num_xy,[20,20],slope,y_intercept,num_seg,rgb_bitwidth,linewidth)
raster_rgb1 = raster_rgb.copy()
sum_rgb1 = raster_rgb.copy()

x_arr, y_arr, rgb_arr,v_arr,raster_rgb1 = gen_xy_input(rgb_array_3d,num_xy,[20,80],-1,y_intercept,num_seg,rgb_bitwidth,linewidth)


raster_cir = gen_circle(rgb_array_3d,[50,50],20)

sum_rgb1 = raster_rgb + raster_rgb1+raster_cir


#plot_pixel(rgb_array)
#print(str(nrows)+"by"+ str(ncols)+ "raster RGB array:")

rgb_aa_3d = anti_aliasing_3d(nrows,ncols,sum_rgb1,30)

plot_pixel(rgb_aa_3d) 




