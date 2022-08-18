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
        self.x = vsc.rand_bit_t(32)
        self.y = vsc.rand_bit_t(32)

    # Pyramid with hole
    @vsc.constraint
    def ab_c(self):
        self.x >= 0
        self.y >= 0
        self.x <= 60
        self.y <= 60
        # NOTE These hole constraints don't work like the mirror SV constraints do.
        # And applying the not across them changes it?
        # not (self.x >= 5 and self.x <= 10 and self.y >= 5 and self.y <= 10)
        # self.x < 5 or self.x > 10 or self.y < 5 or self.y > 10
        self.x + self.y <= 50

    # Quarter circle constraint
    # @vsc.constraint
    # def ab_c(self):
    #     self.a >= 0
    #     self.b >= 0
    #     self.a <= 60
    #     self.b <= 60
    #     self.a * self.a + self.b * self.b <= 50*50


# Hard coded mirror of pyvsc triangle constraints
def triangle_constraints(x, y):
    return x >= 0 and \
           y >= 0 and \
           x <= 60 and \
           y <= 60 and \
           x + y <= 50
           # not (x >= 5 and x <= 10 and y >= 5 and y <= 10) and \


# Create an instance of the item class
my_item_i = my_item_c()

# Empty 2D plane
nx = 60
ny = 60
data = np.zeros((nx, ny))

# Stats for py_rand hit ratio
hits = 0
tries = 0


def py_rand():
    global hits, tries

    while True:
        a = random.randrange(0,nx)
        b = random.randrange(0,ny)
        tries += 1

        if triangle_constraints(a, b):
            hits += 1
            break
    
    return a, b


def pyvsc_rand():
    my_item_i.randomize()
    return my_item_i.x, my_item_i.y


def process_stats(data):
    sorted_data = np.sort(np.array(data).ravel())[::-1]
    sorted_data = [int(x) for x in sorted_data]
    sorted_data = list(filter(lambda x: x > 0, sorted_data))
    print(f'Upper 10 values: {sorted_data[:10]}')
    print(f'Lower 10 values: {sorted_data[-10:]}')
    if tries: print(f'Hit Ratio: {hits}/{tries}')

    fig, (ax0, ax1) = plt.subplots(1, 2)
    fig.suptitle('Distribution Analysis')
    fig.set_size_inches(10, 5)

    ax0.imshow(data, cmap='hot', interpolation='nearest')
    ax0.set_title('Heatmap')

    ax1.hist(sorted_data, bins=20)
    ax1.set_title('Histogram')
    ax1.set_xlabel('hits')
    ax1.set_ylabel('count')
    ax1.set_yscale('log')

    plt.show()


# Load csv file and process stats
def process_save():
    data = np.loadtxt('data.csv', delimiter=',')
    process_stats(data)


# Measure time taken for N randomization calls, then show heatmap
def measure_perf(rands, func):
    start_time = time.time()

    for i in range(rands):
        x, y = func()
        data[x][y] += 1

    elapsed_time = time.time() - start_time
    rands_per_s = rands / elapsed_time
    print(f'--- {elapsed_time} seconds ---')
    print(f'--- {rands_per_s} rands per second ---')

    # Save data off
    np.savetxt('data.csv', data, delimiter=',')

    process_stats(data)


# Show heatmap generated on the fly
def vsc_animation(func, vmax):
    fig = plt.figure()

    im = plt.imshow(data, cmap='hot', interpolation='nearest', vmin=0, vmax=vmax)

    def init():
        im.set_data(np.zeros((nx, ny)))

    def animate(i):
        for _ in range(10):
            x, y = func()
            data[x][y] += 1
        im.set_data(data)
        return im

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=nx * ny, interval=0)

    plt.show()


# Uncomment to see live animation that goes forever
# vsc_animation(py_rand, 10)
# vsc_animation(pyvsc_rand, 10)

# Uncomment to run N times and measure performance + plot of data
# Run for 100,000 or more to really see funky patterns pyvsc generates
# py_rand uses the Python random library and hard coded conditional
# pyvsc_rand uses the pyvsc randomization
# measure_perf(100000, py_rand)
measure_perf(1000, pyvsc_rand)

# Uncomment to load data.csv and reprocess it
# process_save()