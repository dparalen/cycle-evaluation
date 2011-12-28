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
from CyclicSymbolicBoundedLTLEvaluation import OscillationFactory
import ExpressionEvaluation as ee

def simMap(X):
	return Bayramov(X, timeSpace)

def fltMap(sim):
	return ChFilter(sim.result.T, filter_)

def cycMap(flt):
	return CycleDetect(flt.result , epsilon=array([0.001,0.0001,0.0005]))

if __name__ == "__main__":
	logging.basicConfig(level=logging.WARNING)
	# create a regular grid of init value combinations: 6x6x6 3D
	Z = mgrid[0.0015:0.0045:0.0005, 0.00095:0.00665:0.00095, 0.0038:0.0494:0.0076]
	# reshape to a list of 3D points
	Z.shape = 3, 216
	# create a time "axis"
	timeSpace = linspace(0, 960, 9600)
	# create a filter representation
	filter_ = array([[],[0.006],[]])
	# compute
	p = Pool(processes=16)
	simData = p.map(simMap, Z.T, chunksize=8)
	fltData = p.map(fltMap, simData, chunksize=8)
	cycData = p.map(cycMap, fltData, chunksize=8)
	result = array([array([x.start, x.length]) for x in cycData])
	# display the simulations
	fig = pyplot.figure()
	ax = Axes3D(fig)
	#for ba in simData:
	#	ax.plot3D(ba.result.T[0], ba.result.T[1], ba.result.T[2])
	ax.set_xlabel('y')
	ax.set_ylabel('x')
	ax.set_zlabel('z')
	# check oscillation of x_1 > 0.006
	x_1 = 1
	gt = ee.Greater()
	n = ee.NameAtom(x_1)
	v = ee.ValueAtom(0.006)
	ne = ee.AtomExpression(n)
	ve = ee.AtomExpression(v)
	gte = ee.BinaryOperatorExpression(gt, ne, ve)
	oe = OscillationFactory(gte)
	print "oe: %s" % str(oe)
	for i in xrange(216):
		c = cycData[i]
		#ax.plot3D(fltData[i].result.T[0], fltData[i].result.T[1], fltData[i].result.T[2], c="b")
		if c.length > 0:
			ue = oe(0, c.length, c.start)
			r = ue(c.a)
			print "Evaluated on seed: %s: %s" % (Z.T[i], r)
			if r:
				ax.plot3D(simData[i].result.T[0], simData[i].result.T[1], simData[i].result.T[2], c="g")
			else:
				ax.plot3D(simData[i].result.T[0], simData[i].result.T[1], simData[i].result.T[2], c="r")
		else:
			print "Evaluated on seed: %s: False" % Z.T[i]
			ax.plot3D(simData[i].result.T[0], simData[i].result.T[1], simData[i].result.T[2], c="k")
	pyplot.show()
