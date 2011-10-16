#!/usr/bin/env python
from Brent import CycleDetect
from lotka_voltera import LotkaVoltera2D
from Filter import ChFilter
from numpy import *
from multiprocessing import Pool
from matplotlib import pyplot
import matplotlib
import copy_reg
import types

# ----: http://bytes.com/topic/python/answers/552476-why-cant-you-pickle-instancemethods
def _pickle_method(method):
	func_name = method.im_func.__name__
	obj = method.im_self
	cls = method.im_class
	if func_name.startswith('__') and not func_name.endswith('__'):
		cls_name = cls.__name__.lstrip('_')
		if cls_name: func_name = '_' + cls_name + func_name
	return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
	for cls in cls.mro():
		try:
			func = cls.__dict__[func_name]
		except KeyError:
			pass
		else:
			break
		return func.__get__(obj, cls)

copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)
# ----:

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

class Evaluation(object):
	def __init__(self, space, filter_, time, processes=16,
			simType=LotkaVoltera2D, epsilon = 0.5, chunksize=1024):
		self.simType = simType
		self.processes = processes
		self.filter_ = filter_
		self.space = space
		self.time = time
		self.chunksize = chunksize
		p = Pool(processes=self.processes)
		self.simData = p.map(self.simMap, self.space, self.chunksize)
		self.fltData = p.map(self.fltMap, self.simData, self.chunksize)
		self.cycData = p.map(self.cycMap, self.fltData, self.chunksize)
		print self.cycData
		self.result = array([array([x.start, x.length]) for x in self.cycData])
	def simMap(X0):
		return self.simType(X0, self.time)
	def fltMap(sim):
		return ChFilter(sim.result.T, self.filter_)
	def cycMap(flt):
		return CycleDetect(flt.result, epsilon=self.epsilon)

if __name__ == "__main__":
	# create a regular grid of init value combinations
	iX, iY = meshgrid(range(1,11), range(1,11))
	Z = array([iX, iY])
	# make it a "list of pairs"
	Z.shape = 2, 100
	# create a time "axis"
	timeSpace = linspace(0, 10, 2000)
	# create a filter representation
	filter_ = array([[5.0, 2.5], [2.5, 5.0]])
	#p = Pool(processes=16)
	#simData = p.map(simMap, Z.T)
	#fltData = p.map(fltMap, simData)
	#cycData = p.map(cycMap, fltData)
	#result = array([array([x.start, x.length]) for x in cycData])
	evaluation = Evaluation(Z.T, filter_, timeSpace)
	# create a histogram of the data
	histogram = Histogram2D(evaluation.result.T)
	hplot = histogram.plot
	#print histogram.histogram
	pyplot.show()




