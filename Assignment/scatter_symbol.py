"""
==============
Scatter Symbol
==============

"""
from matplotlib import pyplot as plt
import numpy as np
import matplotlib


# Plotting and animation
from matplotlib import animation, rc
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Fixing random state for reproducibility
'''
np.random.seed(19680801)


x = np.arange(0.0, 50.0, 2.0)
y = x ** 1.3 + np.random.rand(*x.shape) * 30.0
s = np.random.rand(*x.shape) * 80 + 50

plt.scatter(x, y, s, c="g", alpha=0.5, marker=r'$\clubsuit$',
            label="Luck")
plt.xlabel("Leprechauns")
plt.ylabel("Gold")
plt.legend(loc=2)
plt.show()
'''
'''
# Interactive plotting
import ipywidgets

from ipywidgets import interact

# Viewing animations in the notebook
from IPython.display import HTML

# Plotting in 3D
from mpl_toolkits.mplot3d import axes3d

# Viewing .gif animations in the notebook
from IPython.display import Image
from IPython.display import display

x = [-1, 3, 4, 8 , 10]
f = [-1, -2, 7, 13 , 1]
#plt.scatter(x,f)
plt.plot(x,f)

plt.show()

'''


from scipy.stats import linregress

def fitValue(x,y):
	yfit =[]
	for num_x in x:
		yfit_res = float(m) * num_x + c
		yfit.append(yfit_res)
	return yfit

x = [-1, 3, 4, 8 , 10]
y = [-1, -2, 7, 13 , 1]
m, c, r_value, p_value, std_err = linregress(x, y)

yfit_list = fitValue(x,y)

# plot a scatter plot by setting 'o' as the marker 
a = plt.figure(1)
plt.plot(x, y, 'ro', label='experiment data')

# plot the fitted linear function 
#plt.legend(loc=-3)
b = plt.figure(2)	
plt.plot(x, yfit_list, 'r--');
a.show()
b.show()
input("Please press enter to close the plots ")