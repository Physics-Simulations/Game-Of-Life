import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import product

def init_world_rand(p, size):
	"""
	Init the world.

	Parameters
	----------
	p:	int, probability that a site is filled
	size: (int, int), dimesions of the grid

	Returns
	-------
	2d array
	"""

	world = np.zeros(size)

	world[np.random.random(size) < p] = 1

	return world


fig, ax = plt.subplots()
data = init_world_rand(0.7, (100, 100))

# creates a glider in the middle
# data = np.zeros((100, 100)) 
# data[50, 50] = 1
# data[50, 51] = 1
# data[51, 51] = 1
# data[51, 52] = 1
# data[52, 50] = 1

im = plt.imshow(data, interpolation='none', cmap='gnuplot')

def count_neighbours(A):
	""" Counts the neighbours of all sites, including diagonal """

	l = [(axis, direction, np.roll(A, direction, axis=axis)) for axis, direction in product([0,1], [1, -1])]
	nn = []
	for axis, direction, M in l:
		nn.append(M)
		nn.append(np.roll(M, - (-1)**axis * direction, axis=(axis+1) % 2))

	return np.sum(nn, axis=0)

def init():
	im.set_data(data)
	return im, 

def frame(k):
	nn = count_neighbours(data)

	# conditions taken from
	# https://bitstorm.org/gameoflife/
	populated = (data == 1)
	cond = (populated & ((nn == 2) | (nn == 3))) | (~populated & (nn == 3))
	
	data[cond] = 1
	data[~cond] = 0

	im.set_data(data)

	return im, 


ani = FuncAnimation(fig, frame, frames=range(1000),
                    init_func=init, blit=True)
plt.show()