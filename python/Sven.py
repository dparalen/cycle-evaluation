#!/usr/bin/env python
# a remake of a cycle detector originally found in:
# 	https://github.com/sybila/parasim
# from numpy import array, ndarray, empty, PINF NINF
import numpy
import collections


class CycleDetect(object):
	def __init__(self, data, maximaLen=128, minimaLen=128, epsilon=0.001):
		if not isinstance(data, numpy.ndarray):
			raise TypeError("Attribute has to be a numpy array instance; got: %s instead" % type(data))
		self.data = data
		self.epsilon = epsilon
		self.maxima = collections.deque(maxlen=maximaLen)
		self.minima = collections.deque(maxlen=minimaLen)
		self.start = 0
		self.length = 0
		self._detect()
	def _detect(self):
		p1 = 1
		p2 = 0
		for x in xrange(2, self.data.shape[-1]):
			if self._gt(p2, p1) and self._gt(x, p1):
				# new minimum at p1
				if self._compute(self._locate(self.minima, p1), p1):
					# cycle detected
					return
				self.minima.append(p1)
			if self._lt(p2, p1) and self._lt(x, p1):
				# new maximum at p1
				if self._compute(self._locate(self.maxima, p1), p1):
					# cycle detected
					return
				self.maxima.append(p2)
			p2 = p1
			p1 = x
	def _locate(self, data, index):
		# locate and index in data via the self._eq method
		return filter(lambda x: self._eq(x, index), data)
	def _compute(self, data, index):
		# compute self.start self.lengt if data contains an index
		if data:
			self.start = data[-1]
			self.length = index - self.start
			return True
		return False
	def _gt(self, a, b):
		if any(self.data.T[a] > self.data.T[b]):
			return True
		return False
	def _lt(self, a, b):
		if any(self.data.T[a] < self.data.T[b]):
			return True
		return False
	def _eq(self, a, b):
		diff = self.data.T[a] - self.data.T[b]
		if any(abs(diff) > self.epsilon):
			return False
		return True
	@property
	def indexes(self):
		return range(self.start, self.length)

	@property
	def result(self):
		return self.data[...,self.indexes]



if __name__ ==  "__main__":
	from Filter import ChFilter
	from Lotka_Volterra import LotkaVolterra2D
	from numpy import *
	import pylab, logging, sys

	logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
	init = array([10, 5])
	dimValues = array([[5.0, 2.5], [2.5, 5.0]])
	time = linspace(0, 120, 120000)
	lv=LotkaVolterra2D(init, time)
	print lv.result.shape
	print lv.result
	f = ChFilter(lv.result.T, dimValues)
	fc = CycleDetect(f.result, epsilon=0.3)
	findexes = fc.indexes
	print findexes
	print fc.start, fc.length
	c = CycleDetect(lv.result, epsilon=0.3)
	indexes = c.indexes
	pylab.plot(lv.result.T[0], lv.result.T[1], 'g.', f.result[0], f.result[1], 'r.',
			lv.result.T[...,indexes][0], lv.result.T[...,indexes][1], 'b.',
			f.result[...,findexes][0], f.result[...,findexes][1], 'rs')
	print c.start, c.length
	pylab.show()
