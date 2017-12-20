#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pylab 

A = np.loadtxt('../../sample_data/sample_data.dat')
print(A)

plt.plot(A[0], A[1])

pylab.show()