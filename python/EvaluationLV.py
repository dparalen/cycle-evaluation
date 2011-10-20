#!/usr/bin/env python
#from Brent import CycleDetect
from Sven import CycleDetect
from Lotka_Volterra import LotkaVolterra2D
from Filter import ChFilter
from numpy import *
from multiprocessing import Pool
from matplotlib import pyplot
from Histogram import Histogram2D
import matplotlib

def simMap(X):
	return LotkaVolterra2D(X, timeSpace)

def fltMap(sim):
	return ChFilter(sim.result.T, filter_)

def cycMap(flt):
	return CycleDetect(flt.result, epsilon=0.03)

if __name__ == "__main__":
	# create a regular grid of init value combinations
	iX, iY = meshgrid(linspace(1,11,100), linspace(1,11,100))
	Z = array([iX, iY])
	# make it a "list of pairs"
	Z.shape = 2, 10000
	# create a time "axis"
	timeSpace = linspace(0, 10, 2000)
	# create a filter representation
	filter_ = array([linspace(1, 11, 4),linspace(1, 11, 4)])
	p = Pool(processes=16)
	simData = p.map(simMap, Z.T, chunksize=8)
	fltData = p.map(fltMap, simData, chunksize=8)
	cycData = p.map(cycMap, fltData, chunksize=8)
	result = array([array([x.start, x.length]) for x in cycData])
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
	#print histogram.histogram
	print starts
	print lengths
	print sl
	print len(sl)
	pyplot.show()
