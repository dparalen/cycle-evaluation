#!/usr/bin/env python
from Brent import CycleDetect
#from Sven import CycleDetect
from Wilhelm import Wilhelm2D
from Filter import ChFilter
from Histogram import Histogram2D
from numpy import *
from multiprocessing import Pool
from matplotlib import pyplot
import matplotlib, os, logging, pylab
from AcyclicSymbolicBoundedLTLEvaluation import Finally,LTLUnaryOperatorExpression
import ExpressionEvaluation as ee

def simMap(X):
	return Wilhelm2D(X, timeSpace)

def fltMap(sim):
	return ChFilter(sim.result.T, filter_)

def cycMap(flt):
	return CycleDetect(flt.result )#, epsilon=0.5)

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	# create a regular grid of init value combinations
	iX, iY = meshgrid(linspace(-3., 3., 3), linspace(-3., 0., 3))
	Z = array([iX, iY])
	# make it a "list of pairs"
	Z.shape = 2, 9
	# create a time "axis"
	timeSpace = linspace(0, 2, 2000)
	# create a filter representation
	filter_ = array([[5],[1]])
	p = Pool(processes=16)
	simData = p.map(simMap, Z.T, chunksize=8)
	fltData = p.map(fltMap, simData, chunksize=8)
	cycData = p.map(cycMap, fltData, chunksize=8)
	result = array([array([x.start, x.length]) for x in cycData])
#	for x in simData:
#		pylab.plot(x.result.T[0], x.result.T[1], 'g,')
	for x in fltData:
		pylab.plot(x.result[0], x.result[1], 'rx')

	F = Finally()
	gt = ee.Greater()
	an = ee.And()
	#vx_0 = slice([0]) # the first dimension
	x_0 = 0
	n = ee.NameAtom(x_0)
	v = ee.ValueAtom(5.)
	ne = ee.AtomExpression(n)
	ve = ee.AtomExpression(v)
	gte = ee.BinaryOperatorExpression(gt, ne, ve)
	x_1 = 1
	n1 = ee.NameAtom(x_1)
	v1 = ee.ValueAtom(1.)
	ne1 = ee.AtomExpression(n1)
	ve1 = ee.AtomExpression(v1)
	gte1 = ee.BinaryOperatorExpression(gt, ne1, ve1)
	ae = ee.NAryOperatorExpression(an, [gte, gte1])
	ex = LTLUnaryOperatorExpression(F, ae)
	print "The expression: %s" % str(ex)
	for i in xrange(9):
		f= fltData[i]
		l = len(f.result.T)
		if l > 0:
			ue = ex(0, l)
			print "Unfolded for len: %s: %s" % (l, str(ue))
			r = ue(f.result)
			print "Evaluated on seed: %s: %s" % (Z.T[i], str(r))
			if r:
#				pylab.plot(simData[i].result.T[0], simData[i].result.T[1], 'b,')
				pylab.plot(Z.T[i][0], Z.T[i][1], 'gs')
			else:
				pylab.plot(Z.T[i][0], Z.T[i][1], 'rs')
				pylab.plot(simData[i].result.T[0], simData[i].result.T[1], 'r,')
		else:
			ue = ex(0, 1)
			print "Unfolded for len: 1: %s" % str(ue)
			r = ue(Z.T[i])
			print "Evaluated on seed: %s: %s" % (Z.T[i], str(r))
			if r:
				pylab.plot(Z.T[i][0], Z.T[i][1], 'gs')
#				pylab.plot(simData[i].result.T[0], simData[i].result.T[1], 'b,')
			else:
				pylab.plot(Z.T[i][0], Z.T[i][1], 'rs')
				pylab.plot(simData[i].result.T[0], simData[i].result.T[1], 'r,')
	pyplot.show()
