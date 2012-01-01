#!/usr/bin/env python
#from Brent import CycleDetect
from Brent import CycleDetect
from Lotka_Volterra import LotkaVolterra2D
from Filter import ChFilter
from numpy import *
from multiprocessing import Pool
from matplotlib import pyplot
from Histogram import Histogram2D
import matplotlib, logging, os, pylab
from CyclicSymbolicBoundedLTLEvaluation import OscillationFactory
import ExpressionEvaluation as ee

def simMap(X):
	return LotkaVolterra2D(X, timeSpace)

def fltMap(sim):
	return ChFilter(sim.result.T, filter_)

def cycMap(flt):
	return CycleDetect(flt.result, epsilon=0.03)

if __name__ == "__main__":
	logging.basicConfig(level=logging.WARNING)
	# create a regular grid of init value combinations
	iX, iY = meshgrid(linspace(1,11,5), linspace(1,11,5))
	Z = array([iX, iY])
	# make it a "list of pairs"
	Z.shape = 2, 25
	# create a time "axis"
	timeSpace = linspace(0, 10, 4000)
	# create a filter representation
	filter_ = array([[],[5.4]])
	p = Pool(processes=16)
	simData = p.map(simMap, Z.T, chunksize=8)
	fltData = p.map(fltMap, simData, chunksize=8)
	cycData = p.map(cycMap, fltData, chunksize=8)
	for x in simData:
		pylab.plot(x.result.T[0], x.result.T[1], 'g,')
	for x in fltData:
		pylab.plot(x.result[0], x.result[1], 'rx')

	# check oscillation of x_1 > 5.4
	x_1 = 1
	gt = ee.Greater()
	n = ee.NameAtom(x_1)
	v = ee.ValueAtom(5.4)
	ne = ee.AtomExpression(n)
	ve = ee.AtomExpression(v)
	gte = ee.BinaryOperatorExpression(gt, ne, ve)
	oe = OscillationFactory(gte)
	print "oe: %s" % str(oe)
	for i in xrange(25):
		c = cycData[i]
		if c.length > 0:
			ue = oe(0, c.length, c.start)
			r = ue(c.a)
			print "Evaluated on seed: %s: %s" % (Z.T[i], r)
			if r:
				pylab.plot(Z.T[i][0], Z.T[i][1], 'gs')
			else:
				pylab.plot(Z.T[i][0], Z.T[i][1], 'rs')
		else:
			print "Evaluated on seed (c.length <= 0): %s: False" % Z.T[i]
			pylab.plot(Z.T[i][0], Z.T[i][1], 'ms')
			pass
	pyplot.show()
