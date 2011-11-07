#!/usr/bin/env python
#from Sven import CycleDetect
from Brent import CycleDetect
from Bayramov import Bayramov
from Filter import ChFilter
from Histogram import Histogram2D
from numpy import *
import numpy as np
from multiprocessing import Pool
from matplotlib import pyplot
import matplotlib, logging, os, pylab
from mpl_toolkits.mplot3d.axes3d import Axes3D
from ConstArrays import Epsilon, Seeds
import Plugins as pl

class ByEpsilonScaled(Epsilon):
	# scaled epsilon for Bayramov cycle-detector in 3D
	_scales = [1., 10., 5.]

class ByEpsilonNonScaled(Epsilon):
	# non-scaled epsilon for Bayramov cycle-detector in 3D
	_scales = [1.]

class ByHundredSeeds(Seeds):
	# create a regular grid of init value combinations: 6x6x6 3D
	_slice = (slice(0.0015,0.0045,0.0005), \
			slice(0.00095,0.00665,0.00095), \
			slice(0.0038,0.0494,0.0076))
	_shape = 3, 216

class ByThousandSeeds(Seeds):
	# create a regular grid of init value combinations: 10x10x10 3D
	_slice = (slice(0.0015,0.0065,0.0005), \
			slice(0.00095,0.01045,0.00095), \
			slice(0.0038,0.0798,0.0076))
	_shape = 3, 1000

class ByTEvaluation(object):
	# the plugin interface
	def __init__(self):
		self.seeds = ByThousandSeeds
		self.time = np.linspace(0, 960, 9600)
		# G((y > 0.001 => F(y <= 0.001)) && (y <= 0.001 => F(y > 0.001)))
		self.one_ap_filter = array([[],[0.001],[]])
		self.four_ap_filter = array([[0.01],[0.001],[0.0005, 0.0001]])
		self.sixteen_ap_filter = array([np.linspace(0.0020, 0.0065, 5), \
				np.linspace(0.0095, 0.01045, 6), lispace(0.0038, 0.0798, 5)])
		
class ByHEvaluation(object):
	def __init__(self):
		self.seeds = ByHundredSeeds
		self.time = np.linspace(0, 960, 9600)
		self.one_ap_filter = array([[], [0.001], []])
		self.four_ap_filter = array([[0.01], [0.001], [0.0005, 0.0001]])
		self.sixteen_ap_filter = array([np.linspace(0.0015, 0.0045, 5), \
		        np.linspace(0.0095, 0.00665, 6),\
		        np.linspace(0.0038, 0.0494, 5)])


class BySHE(pl.Scaled, pl.Hundred, pl.Evaluation3D, ByHEvaluation):
	def __init__(self):
		ByHEvaluation.__init__(self)
		self.epsilon = ByEpsilonScaled

class ByNHE(pl.NonScaled, pl.Hundred, pl.Evaluation3D, ByHEvaluation):
	def __init__(self):
		ByHEvaluation.__init__(self)
		self.epsilon = ByEpsilonNonScaled

class ByNTE(pl.NonScaled, pl.Thousand, pl.Evaluation3D, ByTEvaluation):
	def __init__(self):
		ByTEvaluation.__init__(self)
		self.epsilon = ByEpsilonNonScaled

class BySTE(pl.Scaled, pl.Thousand, pl.Evaluation3D, ByTEvaluation):
	def __init__(self):
		ByTEvaluation.__init__(self)
		self.epsilon = ByEpsilonScaled

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	# create a regular grid of init value combinations: 6x6x6 3D
	Z = mgrid[0.0015:0.0045:0.0005, 0.00095:0.00665:0.00095, 0.0038:0.0494:0.0076]
	# reshape to a list of 3D points
	Z.shape = 3, 216
	# create a time "axis"
	timeSpace = np.linspace(0, 960, 9600)
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




