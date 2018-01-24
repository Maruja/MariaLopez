from pandas import read_csv
from IPython.display import display
import numpy as np
import math
from matplotlib import pyplot as plt
import matplotlib

###############################
 ####Maria Eugenia Lopez ##### 
###############################

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
		Amin = origin_x()  
		Amax = origin_x() + 3000 
		Pb_x= ((Pa_x-Amin)/(Amax-Amin)) * (Bmax-Bmin) + Bmin
		grid_15_x = Pb_x//200
		grid_15_x_list.append(grid_15_x)

		Pa_y = row["GPS_lat"]
		Amin = origin_y()  
		Amax = origin_y() + 3000 
		Pb_y= ((Pa_y-Amin)/(Amax-Amin)) * (Bmax-Bmin) + Bmin
		grid_15_y = Pb_y//200
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


##----------------------------------------
##Part A Assembling a Data Set
##----------------------------------------

##----------------------------------------
##Input and Output: Data Frames

c = 0
plants = read_csv('environmental_survey/plants2017.csv',
	index_col=0)
plants.reset_index(level=0,inplace=True)
plants.drop(plants.index[plants.Plant == 'tree'], inplace=True)
plants.reset_index(drop=True,inplace=True)

##----------------------------------------
##Functions and Data Structures: Boolean Indexing
plants = fully_grown_depuration()
#reseting the index after the depuration 
plants.reset_index(level=0,drop=True,inplace=True)

pH_2017 = read_csv('environmental_survey/pH2017.csv',index_col=0)
pH_2017.reset_index(level=0,inplace=True)

##----------------------------------------
## (1) Mathematical compuation with Numpy

#species = []
winter_mtrx = []
bell_mtrx = []
brush_mtrx = [] 
darley_mtrx = []
grid_15_x_list = []
grid_15_y_list = []

quantisation_Alg(plants)
##----------------------------------------
## (2) Functions 

convert_GPS_lat_long(plants)
#assigning a grid refernce to each data point 
grid_15_x_list,grid_15_y_list = scale(plants)
#display(plants)

winter_mtrx,bell_mtrx,brush_mtrx,darley_mtrx = count_type(plants)

#working with ph data to insert in the Huge list. 
average_pH_mtrx = []
convert_GPS_lat_long(pH_2017)
scale(pH_2017)
average_pH_mtrx = average_pH(pH_2017)
display(plants.head(n=300))	

List_2017 = []
#x_15grid_list = [] 
#y_15grid_list = []


'''for index,row in plants.iterrows():
	x_15grid_list.append(row["x_15grid"])
	y_15grid_list.append(row["y_15grid"])
'''
##----------------------------------------
##(3) Data Structures: Lists 

List_2017 = [grid_15_x_list,grid_15_y_list,average_pH_mtrx,winter_mtrx,bell_mtrx,brush_mtrx,darley_mtrx]
#printing the huge list 
print(List_2017)