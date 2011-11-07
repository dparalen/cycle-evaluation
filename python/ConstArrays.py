#!/usr/bin/env python
import numpy as np

class Seeds(np.ndarray):
	# a constant ndarray to be used as seeds for a simulation
	# subtypes should override the _slice and _shape class attributes
	_slice = slice(0.,0.,1)
	_shape = 0
	def __new__(subtype):
		subarr = np.mgrid[subtype._slice]
		subarr.shape = subtype._shape
		subarr = subarr.view(subtype)
		return subarr
	def __array_finalize__(self, object):
		pass

class Epsilon(np.ndarray):
	# a constant ndarray to be used as precision for cycle detection etc.
	# subtypes should override the _scales list to provide custom scaled Epsilon
	# in multiple dimensions
	_scales = [1.]
	def __new__(subtype, m = 1.):
		subarr = np.array(subtype._scales) * m
		subarr = subarr.view(subtype)
		subarr.m = m
		return subarr
	def __array_finalize__(self, object):
		self.m = getattr(object, 'm', None)

if __name__ == '__main__':
	e = Epsilon(7.)
	print e
	print e.m
