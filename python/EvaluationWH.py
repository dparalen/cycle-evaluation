#!/usr/bin/env python
from Brent import CycleDetect
from Wilhelm import Wilhelm2D
from Filter import ChFilter
from Histogram import Histogram2D
from numpy import *
from multiprocessing import Pool
from matplotlib import pyplot
import matplotlib, os, logging, pylab

def simMap(X):
	return Wilhelm2D(X, timeSpace)

def fltMap(sim):
	return ChFilter(sim.result.T, filter_)

def cycMap(flt):
	return CycleDetect(flt.result, epsilon=0.005)

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	# create a regular grid of init value combinations
	iX, iY = meshgrid(linspace(0., 6., 3), linspace(0., 6., 3))
	Z = array([iX, iY])
	# make it a "list of pairs"
	Z.shape = 2, 9
	# create a time "axis"
	timeSpace = linspace(0, 2, 2000)
	# create a filter representation
	filter_ = array([[4., 4.5, 5., 5.5, 6., 6.5, 7, 7.5],[1]])
	p = Pool(processes=16)
	simData = p.map(simMap, Z.T, chunksize=8)
	fltData = p.map(fltMap, simData, chunksize=8)
	cycData = p.map(cycMap, fltData, chunksize=8)
	result = array([array([x.start, x.length]) for x in cycData])
	for x in simData:
		pylab.plot(x.result.T[0], x.result.T[1], 'g.')
	for x in fltData:
		pylab.plot(x.result[0], x.result[1], 'r.')
	pyplot.show()
	# create a histogram of the data
	histogram = Histogram2D(result.T)
	hplot = histogram.plot
	#print histogram.histogram
	pyplot.show()




