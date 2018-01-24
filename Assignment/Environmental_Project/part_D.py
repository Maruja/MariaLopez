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

from scipy.stats import linregress

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

	df["x_15grid"] = grid_15_x_list
	df["y_15grid"] = grid_15_y_list
	return grid_15_x_list,grid_15_y_list


def origin_x():
	return plants.GPS_lon.min()+((3445-3000)/2)

def origin_y():
	return plants.GPS_lat.min()+((3950-3000)/2)
		

def fully_grown_depuration(number_to_remove=0.50):
	 return plants.loc[plants.height_m > number_to_remove]


def quantisation_Alg(plants):
	global c
	total_d = 0	
	totals = []
	species = []

	Winter=[1.2,3.5,2.0,2.3]
	Bell=[1.8,1.5,1.2,2.3]
	Brush=[0.7,2.1,10.2,1.5]
	Darley=[0.7,2.2,3.1,1.7]
	categories=[Winter,Bell,Brush,Darley]
	categories_str=["Winter","Bell","Brush","Darley"]
	characteristycs = ["height_m","leaf_length_cm","leaf_aspect_ratio","bud_length_cm"]

	for index,row in plants.iterrows():
		totals = []
		for category in categories:
			total_d=0
			for x in range(4):
				d = category[x]-row[characteristycs[x]]
				d = d**2
				total_d = total_d + d
			total = math.sqrt(total_d)
			totals.append(total)
		closest_fit = min(totals)
		index = totals.index(min(totals))
		species.append(categories_str[index])

		c=c+1
	plants["species"] = species


def count_type(df):
	winter_count = np.zeros((15,15))
	bell_count = np.zeros((15,15))
	brush_count = np.zeros((15,15))
	darley_count = np.zeros((15,15))

	for index,row in df.iterrows():
		if (row["x_15grid"] >= 0 and row["x_15grid"] <= 14) and (row["y_15grid"] >= 0 and row["y_15grid"] <= 14):
			if(row["species"] == "Winter"):
				winter_count[int(row["x_15grid"])][int(row["y_15grid"])] += 1
			if(row["species"] == "Bell"):
				bell_count[int(row["x_15grid"])][int(row["y_15grid"])] += 1
			if(row["species"] == "Brush"):
				brush_count[int(row["x_15grid"])][int(row["y_15grid"])] += 1
			if(row["species"] == "Darley"):
				darley_count[int(row["x_15grid"])][int(row["y_15grid"])] += 1
	return winter_count,bell_count,brush_count,darley_count

def fitValue(x,y):
	yfit =[]
	m,c,r_value,p_value,std_err = linregress(x,y)
	for num_x in x:
		yfit_res = float(m) * num_x + c
		yfit.append(yfit_res)
	return yfit,round(m,2),round(c,2)


c=0
annual_data=[]
near_data_PH = [] 
near_data_winter = []
near_data_bell = []
near_data_brush = []
near_data_darley = []
far_data_PH = [] 
far_data_winter = []
far_data_bell = []
far_data_brush = []
far_data_darley = []

years = range(1997,2018)
for year in years:
	print("loading ... ..... ...... year ", year)
	average_pH_mtrx = [] 
	winter_mtrx = []
	bell_mtrx = []
	brush_mtrx = [] 
	darley_mtrx = []
	grid_15_x_list = []
	grid_15_y_list = []
	List_per_year = []

	pH = read_csv("environmental_survey/pH" + str(year) + ".csv",index_col=0)
	pH.reset_index(level=0,inplace=True)
	plants = read_csv("environmental_survey/plants" + str(year) + ".csv")
	plants.reset_index(level=0,inplace=True)
	plants.drop(plants.index[plants.Plant == 'tree'], inplace=True) #getting rid of the trees 
	plants.reset_index(drop=True,inplace=True) # reseting index 
	plants = fully_grown_depuration() # only the ones that are properly grown 
	plants.reset_index(level=0,drop=True,inplace=True) # reseting index 

	## working with Plants Data 
	quantisation_Alg(plants)	#getting the species for each row
	convert_GPS_lat_long(plants)	#converting 
	grid_15_x_list,grid_15_y_list = scale(plants)	#scale 
	#working with PH data 
	convert_GPS_lat_long(pH)
	scale(pH)
	average_pH_mtrx = average_pH(pH)  # getting the mean for each grid 
	winter_mtrx,bell_mtrx,brush_mtrx,darley_mtrx = count_type(plants)  
	# getting each matrix with the count for each grid of plants 

	##getting the near data to plot the 5 different graphs of a point 
	##which are near both plants (14,7) specially philamores plant 
	near_data_PH.append(average_pH_mtrx[14][7])
	near_data_winter.append(winter_mtrx[14][7])
	near_data_bell.append(bell_mtrx[14][7])
	near_data_brush.append(brush_mtrx[14][7])
	near_data_darley.append(darley_mtrx[14][7])

	##getting the near data to plot the 5 different graphs of a point 
	##which are far both plants (4,14) 
	far_data_PH.append(average_pH_mtrx[4][14])
	far_data_winter.append(winter_mtrx[4][14])
	far_data_bell.append(bell_mtrx[4][14])
	far_data_brush.append(brush_mtrx[4][14])
	far_data_darley.append(darley_mtrx[4][14])

	##-----------------------------------------------------------------
	## (1) Control Flow 
	List_per_year = [grid_15_x_list,grid_15_y_list,average_pH_mtrx,winter_mtrx,bell_mtrx,brush_mtrx,darley_mtrx]

	annual_data.append(List_per_year)

##to check how the annual_data looks uncooment this print line 	
#print(annual_data)

##-------------------------------------------------------------------------
## (2) Plotting and Curve Fitting 
#____________________________near to the plants _______________
a = plt.figure(1)

plt.plot(years,near_data_PH, 'b', label="pH_mean")
yfit_list,m,c = fitValue(years,near_data_PH)
plt.plot(years, yfit_list, 'b--', label="y_pH="+str(m)+"x+"+str(c))

plt.plot(years,near_data_winter,'r', label="winter")
yfit_list,m,c = fitValue(years,near_data_winter)
plt.plot(years, yfit_list, 'r--', label="y_winter="+str(m)+"x+"+str(c))

plt.plot(years,near_data_bell,'g', label="bell")
yfit_list,m,c = fitValue(years,near_data_bell)
plt.plot(years, yfit_list, 'g--', label="y_bell="+str(m)+"x+"+str(c))

plt.plot(years,near_data_brush,'k', label="brush")
yfit_list,m,c = fitValue(years,near_data_brush)
plt.plot(years, yfit_list, 'k--', label="y_brush="+str(m)+"x+"+str(c))

plt.plot(years,near_data_darley,'y', label="darley")
yfit_list,m,c = fitValue(years,near_data_darley)
plt.plot(years, yfit_list, 'y--', label="y_darley="+str(m)+"x+"+str(c))


plt.xlabel('$years$', fontsize=10)
plt.ylabel('$avg$', fontsize=10)
plt.legend(loc=2, fontsize=9)
plt.title("Average pH and plant count for each species NEAR plants", fontsize=10);

#______________far away point _______________

b = plt.figure(2)

plt.plot(years,far_data_PH, 'b', label="pH_mean")
yfit_list,m,c = fitValue(years,far_data_PH)
plt.plot(years, yfit_list, 'b--', label="y_pH="+str(m)+"x+"+str(c))

plt.plot(years,far_data_winter,'r', label="winter")
yfit_list,m,c = fitValue(years,far_data_winter)
plt.plot(years, yfit_list, 'r--', label="y_winter="+str(m)+"x+"+str(c))

plt.plot(years,far_data_bell,'g', label="bell")
yfit_list,m,c = fitValue(years,far_data_bell)
plt.plot(years, yfit_list, 'g--', label="y_bell="+str(m)+"x+"+str(c))

plt.plot(years,far_data_brush,'k', label="brush")
yfit_list,m,c = fitValue(years,far_data_brush)
plt.plot(years, yfit_list, 'k--', label="y_brush="+str(m)+"x+"+str(c))

plt.plot(years,far_data_darley,'y', label="darley")
yfit_list,m,c = fitValue(years,far_data_darley)
plt.plot(years, yfit_list, 'y--', label="y_darley="+str(m)+"x+"+str(c))


plt.xlabel('$years$', fontsize=10)
plt.ylabel('$avg$', fontsize=10)
plt.legend(loc=2, fontsize=9)
plt.title("Average pH and plant count for each species FAR from plants", fontsize=10);

input("Press ENTER to appear the plots ..")
a.show()
b.show()
print("READ TO MANAGE PLOTS !!!!!!!!!!!!!!!!!!!\n , to move them select the plot two times....\n" )
input("Press enter to close the plots") 
