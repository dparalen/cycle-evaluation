#!/usr/bin/env python
# from Sven import CycleDetect
from Brent import CycleDetect
from Bayramov import Bayramov
from Filter import ChFilter
from Histogram import Histogram2D
from numpy import *
from multiprocessing import Pool
from matplotlib import pyplot
import matplotlib, logging, os, pylab
from mpl_toolkits.mplot3d.axes3d import Axes3D

def simMap(X):
	return Bayramov(X, timeSpace)

def fltMap(sim):
	return ChFilter(sim.result.T, filter_)

def cycMap(flt):
	return CycleDetect(flt.result , epsilon=0.0001)

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	# create a regular grid of init value combinations: 6x6x6 3D
	Z = mgrid[0.0015:0.0045:0.0005, 0.00095:0.00665:0.00095, 0.0038:0.0494:0.0076]
	# reshape to a list of 3D points
	Z.shape = 3, 216
	# create a time "axis"
	timeSpace = linspace(0, 960, 9600)
	# create a filter representation
	filter_ = array([[],[0.001],[]])
	# compute
	p = Pool(processes=16)
	simData = p.map(simMap, Z.T, chunksize=8)
	fltData = p.map(fltMap, simData, chunksize=8)
	cycData = p.map(cycMap, fltData, chunksize=8)
	result = array([array([x.start, x.length]) for x in cycData])
	# display the simulations
	fig = pyplot.figure()
	ax = Axes3D(fig)
	for ba in simData:
		ax.plot3D(ba.result.T[0], ba.result.T[1], ba.result.T[2])
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')
	pyplot.show()
	# some stats
	starts = {}
	lengths = {}
	sl = {}
	for x, y in result:
		try:
			starts[x] += 1
		except KeyError:
			starts[x] = 1
		try:
			lengths[y] += 1
		except KeyError:
			lengths[y] = 1
		try:
			sl["%s_%s" % (x,y)] += 1
		except KeyError:
			sl["%s_%s" % (x, y)] = 1

	# create a histogram of the data
	histogram = Histogram2D(result.T)
	hplot = histogram.plot
	# print histogram evaluation
	print starts
	print lengths
	print sl
	print len(sl)
	pyplot.show()




