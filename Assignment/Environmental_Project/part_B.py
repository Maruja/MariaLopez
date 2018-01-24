from pandas import read_csv
from IPython.display import display
import numpy as np
import math
# Plotting and animation
import matplotlib
from matplotlib import animation, rc
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pylab	

###############################
 ####Maria Eugenia Lopez ##### 
###############################

def average_pH(df):
	matrix = np.zeros((15,15))   
	aux = np.zeros((15,15)) # aux stores the number of plants in this grid area   

	for index,row in df.iterrows():
		if (row["x_15grid"] >= 0 and row["x_15grid"] <= 14) and (row["y_15grid"] >= 0 and row["y_15grid"] <= 14):
			matrix[int(row["x_15grid"])][int(row["y_15grid"])] += float(row["pH"])
			aux[int(row["x_15grid"])][int(row["y_15grid"])] += 1

	for i in range(15):
		for j in range(15):
			if aux[i][j] != 0:
				aux[i][j] = matrix[i][j]/aux[i][j]  # sum of all the pH value / number of plants in this grid 
	return aux

def convert_GPS_lat_long(df):
	for index, row in df.iterrows():
		lat_viejo = row["GPS_lat"]
		latVal = (40008000*row["GPS_lat"])/360
		#res= div*0.001#to convert to Klm
		df.loc[index,"GPS_lat"] = latVal

		lat_radians = math.radians(lat_viejo)
		lonVal = (40075160*row["GPS_lon"])/360
		lonVal = lonVal*math.cos(lat_radians)
		#res = res*0.001
		df.loc[index,"GPS_lon"] = lonVal 

def scale(df):
	Pb_x_list = []
	Pb_y_list = []
	grid_15_x_list = []
	grid_15_y_list = []

	Bmin = 0 
	Bmax = 3000

	for index, row in df.iterrows():
		Pa_x = row["GPS_lon"]
		Amin = origin_x()  #Amin =  12358256.1116
		Amax = origin_x() + 3000 # Amax =12361256.1116

		Pb_x= ((Pa_x-Amin)/(Amax-Amin)) * (Bmax-Bmin) + Bmin
		grid_15_x = Pb_x//200
		Pb_x_list.append(Pb_x)
		grid_15_x_list.append(grid_15_x)


		Pa_y = row["GPS_lat"]
		Amin = origin_y()  #Amin =  12358256.1116
		Amax = origin_y() + 3000 # Amax =12361256.1116
		
		Pb_y= ((Pa_y-Amin)/(Amax-Amin)) * (Bmax-Bmin) + Bmin
		grid_15_y = Pb_y//200

		Pb_y_list.append(Pb_y)
		grid_15_y_list.append(grid_15_y)

	pH["scale_long"] = Pb_x_list
	pH["scale_lat"] = Pb_y_list
	pH["x_15grid"] = grid_15_x_list
	pH["y_15grid"] = grid_15_y_list



def origin_x():
		return pH.GPS_lon.min()+((3445-3000)/2)

def origin_y():
	return pH.GPS_lat.min()+((3950-3000)/2)


##----------------------------------------
##Part B Refining the Data Set and Mapping pH
##----------------------------------------

##----------------------------------------
##(1) Input and Output 
pH = read_csv('environmental_survey/pH2017.csv',
	index_col=0)
pH.reset_index(level=0,inplace=True)

#display(pH.head(n=50))

##----------------------------------------
##(2) Functions
convert_GPS_lat_long(pH)

##----------------------------------------
##(3) Functions and mathematical operators. 

scale(pH)

display(pH.head(n=200))

##----------------------------------------
##(3.) numpy multi-dimensional arrays. 

avg = []
avg = average_pH(pH)

plt.matshow(avg)

plt.colorbar()
plt.title("average_pH per grid")
pylab.show()
plt.savefig('average2_pH.png')



