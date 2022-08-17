#!/usr/bin/env python3

# Testing out interesting 2D constraints to visualize uniform distribution issues
# See end of file for live animation vs performance measurement functions

import vsc
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import random
import time


@vsc.randobj
class my_item_c(object):
    def __init__(self):
        self.a = vsc.rand_bit_t(32)
        self.b = vsc.rand_bit_t(32)

    # Pyramid with hole
    @vsc.constraint
    def ab_c(self):
        self.a >= 0
        self.b >= 0
        self.a <= 60
        self.b <= 60
        # NOTE These hole constraints don't work like the mirror SV constraints do.
        # And applying the not across them changes it?
        # not (self.a >= 5 and self.a <= 10 and self.b >= 5 and self.b <= 10)
        # self.a < 5 or self.a > 10 or self.b < 5 or self.b > 10
        self.a + self.b <= 50

    # Quarter circle constraint
    # @vsc.constraint
    # def ab_c(self):
    #     self.a >= 0
    #     self.b >= 0
    #     self.a <= 60
    #     self.b <= 60
    #     self.a * self.a + self.b * self.b <= 50*50


# Create an instance of the item class
my_item_i = my_item_c()

# Empty 2D plane
nx = 60
ny = 60
data = np.zeros((nx, ny))


# Measure time taken for N randomization calls, then show heatmap
def measure_vsc(rands):
    start_time = time.time()

    for i in range(rands):
        my_item_i.randomize()
        data[my_item_i.a][my_item_i.b] += 1

    elapsed_time = time.time() - start_time
    rands_per_s = rands / elapsed_time
    print(f'--- {elapsed_time} seconds ---')
    print(f'--- {rands_per_s} rands per second ---')

    sorted_data = np.sort(np.array(data).ravel())[::-1]
    sorted_data = [int(x) for x in sorted_data]
    sorted_data = list(filter(lambda x: x > 0, sorted_data))
    print(f'Upper 10 values: {sorted_data[:10]}')
    print(f'Lower 10 values: {sorted_data[-10:]}')

    plt.imshow(data, cmap='hot', interpolation='nearest')
    plt.show()


# Show heatmap generated on the fly
def vsc_animation(vmax=10):
    fig = plt.figure()

    im = plt.imshow(data, cmap='hot', interpolation='nearest', vmin=0, vmax=vmax)

    def init():
        im.set_data(np.zeros((nx, ny)))

    def animate(i):
        my_item_i.randomize()
        data[my_item_i.a][my_item_i.b] += 1
        im.set_data(data)
        return im

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=nx * ny, interval=50)

    plt.show()


# Uncomment to see live animation that goes forever
# vsc_animation(5)

# Uncomment to run N times and measure time/performance + plot of data
# Run for 100,000 or more to really see funky patterns pyvsc generates
measure_vsc(1000)
