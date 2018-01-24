import numpy as np
import pandas as pd
from IPython.display import display
# Plotting and animation
import matplotlib
from matplotlib import animation, rc
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pylab
#%matplotlib inline
'''x = np.array([[8, 7, 6, 8],
              [8, 7, 6, 3],
              [6, 6, 5, 2],
              [4, 3, 2, 1]])

plt.matshow(x)

plt.colorbar()
pylab.show()'''


df2 = pd.DataFrame(np.random.rand(10, 4), columns=['a', 'b', 'c', 'd'])
'''
      a         b         c         d
0  0.758720  0.679408  0.697484  0.699627
1  0.490708  0.490955  0.524889  0.013796
2  0.293530  0.024602  0.046595  0.537699
3  0.763462  0.889153  0.411250  0.403361
4  0.088298  0.743743  0.644973  0.538803
5  0.375303  0.123643  0.259735  0.551388
6  0.989338  0.696026  0.673358  0.702256
7  0.155866  0.289417  0.728621  0.798907
8  0.506304  0.847535  0.804409  0.341783
9  0.382979  0.841379  0.420378  0.811660

'''
display(df2)

df2.plot.scatter(x='a', y='b');
plt.show()

df2.plot.bar()
#df2.plot.bar()
pylab.show()