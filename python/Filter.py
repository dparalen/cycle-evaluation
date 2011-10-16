#!/usr/bin/env python
import logging
from numpy import array

logger = logging.getLogger(__name__)

def eval(element, dimValues):
	ret = []
	for e, values in zip(element, dimValues):
		ret.append(False)
		for v in values:
			if e > v:
				ret[-1] = True
	# logger.debug("eval: %s" % ret)
	return ret

class SwitchCmp:
	def __init__(self, old):
		self.old = old

	def __call__(self, new):
		for o, n in zip (self.old, new):
			if o ^ n:
				# logger.debug("switchCmp: changed: (self.old: %s, new: %s)" % (self.old, new))
				self.old = new
				return True
		return False

class ChFilter:
	"""
	filter: filter a NumPy array by dimValues evaluation changes

	dimValues: [[d0v0, d0v1, d0v2], ... [], ... [d1v0, d1v1, ...], ...]
	returns a new array containing only passed original elements
	"""
	def __init__(self, a, dimValues):
		self.a = a
		self.dimValues = dimValues
		sw = SwitchCmp(eval(a[...,0], dimValues))
		self.indexes = filter(lambda x: sw(eval(self.a[...,x], dimValues)), range(1, self.a.shape[-1]))
	@property
	def result(self):
		return self.a[...,self.indexes]

if __name__ == "__main__":
	from numpy import array, arange
	from Lotka_Volterra import LotkaVolterra2D
	import logging, sys

	logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

	time = arange(0.0, 20.0, 0.01)
	init = array([9, 2])
	lv = LotkaVolterra2D(init, time)
	dimValues = array([[5.0, 2.5], [2.0, 1.25]])
	f = ChFilter(lv.result, dimValues)
	print f.result
	print f.indexes
