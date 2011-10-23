#!/usr/bin/env python
# provides Cyclic Symbolic Bounded Evaluation to LTLExpression structures
import LTLExpression as lex
import ExpressionStructure as cex
import numpy as np

class Evaluation(object):
	# denotes a cyclic evaluable object
	def __init__(self, position = 0, start = 0, length = 0):
		self.position = 0
		self.start = 0
		self.length = 0
	@abstractmethod
	def __call__(self, data):
		pass

class AP(cex.AtomExpression, Evaluation):
	# cyclic atomic proposition evaluation
	def __init__(self, anAtom, position, start = 0, length = 0):
		cex.AtomExpression(self, anAtom)
		Evaluation.__init__(self, position, start, length)
	def __call__(self, data):
		assert isinstance(data, np.ndarray)
		return cex.AtomExpression(data[...,self.position])

