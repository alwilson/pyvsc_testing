#!/usr/bin/env python3

# Used for plotting out dist_test.svh output file, plot.csv

from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np

nx = 60
ny = 60
data = np.zeros((nx, ny))

points= np.genfromtxt('plot.csv', delimiter=',')
for p in points:
    data[int(p[0])][int(p[1])] += 1


sorted_data = np.sort(np.array(data).ravel())[::-1]
sorted_data = [int(x) for x in sorted_data]
sorted_data = list(filter(lambda x: x > 0, sorted_data))
print(f'Upper 10 values: {sorted_data[:10]}')
print(f'Lower 10 values: {sorted_data[-10:]}')

plt.imshow(data, cmap='hot', interpolation='nearest')
plt.show()

