#!/usr/bin/env python
# based upon: http://en.wikipedia.org/wiki/Cycle_detection#Brent.27s_algorithm
from numpy import array, ndarray

import logging, sys

logger = logging.getLogger(__name__)

class CycleDetect:
	def __init__(self, a, epsilon=0.001):
		if not isinstance(a, ndarray):
			raise TypeError("Attribute has to be a numpy array instance; got: %s instead" % type(a))
		self.a = a
		self.epsilon = epsilon
		self.length = self._length
		self.start = self._start

	def cmp(self, a, b):
		diff = a - b
		if any(abs(diff) > self.epsilon):
			return False
		return True

	@property
	def _length(self):
		if self.a.shape[-1] <= 1:
			# 1-element array can't contain a cycle
			return 0
		power = lambda_ = 1
		tortoise = 0
		hare = 1
		while hare < self.a.shape[-1] and not self.cmp(self.a[...,tortoise], self.a[...,hare]):
			# logger.debug("  t:%s, h:%s" % (self.a[...,tortoise], self.a[...,hare]))
			if power == lambda_:
				tortoise = hare
				power *= 2
				lambda_ = 0
			hare += 1
			lambda_ += 1
		if hare == self.a.shape[-1]:
			# hit the end, no cycle detected
			return 0
		return lambda_

	@property
	def _start(self):
		mu = tortoise = 0
		hare = self.length
		while self.a.shape[-1] > hare and not self.cmp(self.a[...,tortoise], self.a[...,hare]):
			tortoise +=1
			hare +=1
			mu += 1
		return mu

	@property
	def indexes(self):
		return range(self.start, self.length)

	@property
	def result(self):
		return self.a[...,self.indexes]

if __name__ ==  "__main__":
	from Filter import ChFilter
	from Lotka_Volterra import LotkaVolterra2D
	from numpy import *
	import pylab

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
	c = CycleDetect(lv.result.T)
	indexes = c.indexes
	pylab.plot(lv.result.T[0], lv.result.T[1], 'g.', f.result[0], f.result[1], 'r.',
			lv.result.T[...,indexes][0], lv.result.T[...,indexes][1], 'b.',
			f.result[...,findexes][0], f.result[...,findexes][1], 'rs')
	print c.start, c.length
	pylab.show()
