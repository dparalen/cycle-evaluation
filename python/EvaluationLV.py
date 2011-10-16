#!/usr/bin/env python
from Brent import CycleDetect
from Lotka_Volterra import LotkaVolterra2D
from Filter import ChFilter
from numpy import *
from multiprocessing import Pool
from matplotlib import pyplot
import matplotlib
import copy_reg
import types

class Histogram2D:
	def __init__(self, a, xlabel='length: l', ylabel='start: s',
			title='s/l distribution'):
		self.xmax, self.ymax = amax(a.T, axis=0)
		self.histogram, self.xedges, self.yedges = histogram2d(a[0], a[1],
				normed = True,
			bins=[self.xmax, self.ymax])
		self.extent = [self.yedges[0], self.yedges[-1], self.xedges[-1],
				self.xedges[0]]
		self.xlabel = xlabel
		self.ylabel = ylabel
		self.title = title
	@property
	def plot(self):
		im = pyplot.imshow(self.histogram, extent=self.extent,
				norm=matplotlib.colors.Normalize(vmin=0.,vmax=1.),
				interpolation='bicubic'
		)
		im.axes.set_ylabel(self.ylabel)
		im.axes.set_xlabel(self.xlabel)
		im.axes.set_title(self.title)
		im.colorbar = pyplot.colorbar()
		return im

def simMap(X):
	return LotkaVolterra2D(X, timeSpace)

def fltMap(sim):
	return ChFilter(sim.result.T, filter_)

def cycMap(flt):
	return CycleDetect(flt.result, epsilon=0.1)

if __name__ == "__main__":
	# create a regular grid of init value combinations
	iX, iY = meshgrid(range(1,11), range(1,11))
	Z = array([iX, iY])
	# make it a "list of pairs"
	Z.shape = 2, 100
	# create a time "axis"
	timeSpace = linspace(0, 10, 2000)
	# create a filter representation
	filter_ = array([[5.0, 2.5, pi], [2.5, 5.0, pi]])
	p = Pool(processes=16)
	simData = p.map(simMap, Z.T, chunksize=8)
	fltData = p.map(fltMap, simData, chunksize=8)
	cycData = p.map(cycMap, fltData, chunksize=8)
	result = array([array([x.start, x.length]) for x in cycData])
	# create a histogram of the data
	histogram = Histogram2D(result.T)
	hplot = histogram.plot
	#print histogram.histogram
	pyplot.show()




