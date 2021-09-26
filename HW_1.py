# -*- coding: utf-8 -*-
"""
Assignment 1
"""

# Import packages
import matplotlib.pyplot as plt
import numpy as np

# Create graph of sin(x) and cos(x)
x = np.arange(0,4*np.pi-1,0.1)
y = np.sin(x)
z = np.cos(x)

plt.plot(x, y, x, z)
plt.xlabel('x values from 0 to 4pi')
plt.ylabel('sin(x) and cos(x)')
plt.title('Plot of sin(x) and cos(x) from 0 to 4pi')
plt.legend(['sin(x)', 'cos(x)'])
plt.show()
