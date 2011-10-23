#!/usr/bin/env python
# provides Acyclic Symbolic Bounded Evaluation to LTLExpression structures
import LTLExpression as lex
import ExpressionStructure as cex
import numpy as np

class Evaluation(object):
	# denotes an acyclic evaluable object
	def __init__(self, position = 0, start = 0):
		self.position = 0
		self.start = 0
	@abstractmethod
	def __call__(self, data):
		pass

class AP(cex.AtomExpression, Evaluation):
	# acyclic atomic proposition evaluation
	def __init__(self, anAtom, position = 0, length = 0):
		cex.AtomExpression(self, anAtom)
		Evaluation.__init__(self, position, length)
	def __call__(self, data):
		assert isinstance(data, np.ndarray)
		return cex.AtomExpression.__call__(self, data[...,self.position])



