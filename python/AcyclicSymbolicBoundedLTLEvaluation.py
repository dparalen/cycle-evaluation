#!/usr/bin/env python
# provides Acyclic Symbolic Bounded Evaluation to LTLExpression structures
import LTLExpression as le
import ExpressionEvaluation as ee
import ExpressionStructure as ex
import numpy as np
import itertools as it
import logging, os
from Cached import CachedCall, CachedNew

logger = logging.getLogger(__name__)

# The operators define the bounded acyclic semantics for an LTL structure
# instance

def _ltl_expressions(Expressions):
	return filter(lambda x: isinstance(x, le.LTL), Expressions)

def _split_expressions(Expressions):
	# returns a tuple of ltl and other expressions found in Expressions
	ltl = _ltl_expressions(Expressions)
	ret = ltl, filter(lambda x: not isinstance(x, le.LTL), Expressions)
	logger.debug("_split_expressions: %s" % repr(ret))
	return ret

def _ltl_expression(Expression):
	return isinstance(Expression, le.LTL)

class And(le.And, CachedCall):
	def _cached(self, Expressions, position=0, length=0):
		ltl_expressions, other_expressions = _split_expressions(Expressions)
		return ee.NAryOperatorExpression(ee.And(), Expressions = map(lambda x: x(position,
			length), ltl_expressions) + map(lambda x: _EvaluationExpression(x,
				position), other_expressions))

class Or(le.Or, CachedCall):
	def _cached(self, Expressions, position = 0, length = 0):
			ltl_expressions, other_expressions = _split_expressions(Expressions)
			return ee.NAryOperatorExpression(ee.Or(), Expressions = map(lambda x: x(position,
			length), ltl_expressions) + map(lambda x: _EvaluationExpression(x,
				position), other_expressions))

class Not(le.Not, CachedCall):
	def _cached(self, Expression, position = 0, length = 0):
		if _ltl_expression(Expression):
			return ee.UnaryOperatorExpression(ee.Not(), Expression(position,
				length))
		return  ee.UnaryOperatorExpression(ee.Not(), _EvaluationExpression(
			Expression, position))

class Next(le.Next, CachedCall):
	def _cached(self, Expression, position = 0, length = 0):
		if position >= length:
			# return "False" if on end
			return ee.AtomExpression(ee.FalseAtom())
		if _ltl_expression(Expression):
			return Expression(position + 1, length)
		return _EvaluationExpression(Expression, position)

class Globally(le.Globally):
	# can't be cached
	def __call__(self, Expression, position = 0, length = 0):
		# Globally always "False" on acyclic trajectories
		return ee.AtomExpression(ee.FalseAtom())

class Finally(le.Finally, CachedCall):
	def _cached(self, Expression, position = 0, length = 0):
		if _ltl_expression(Expression):
			logger.debug("Finally: LTL expansion")
			return ee.NAryOperatorExpression(ee.Or(), Expressions = [ Expression(x, length)
				for x in xrange(position, length)])
		logger.debug("Finally: non-LTL expansion: %s" % str(Expression))
		return ee.NAryOperatorExpression(ee.Or(), Expressions = [ _EvaluationExpression(Expression,
			x) for x in xrange(position, length)])

class Until(le.Until, CachedCall):
	def _cached(self, LeftExpression, RightExpression, position = 0, length =
			0):
		logger.debug("Until: _cached: %s, %s" % (LeftExpression, RightExpression))
		if _ltl_expression(LeftExpression) and \
				_ltl_expression(RightExpression):
			return ee.NAryOperatorExpression(ee.Or(), Expressions = \
					[ee.NAryOperatorExpression(ee.And(), Expressions = \
						[RightExpression(j,length)] +
						[LeftExpression(n, length) for n in xrange(position, j)])
							for j in xrange(position, length)])
		if _ltl_expression(LeftExpression):
			return ee.NAryOperatorExpression(ee.Or(),
					Expressions = [ee.NAryOperatorExpression(ee.And(), Expressions = \
							[_EvaluationExpression(RightExpression, j)] +
						[LeftExpression(n, length) for n in xrange(position, j)])
							for j in xrange(position, length)])
		if _ltl_expression(RightExpression):
			return ee.NAryOperatorExpression(ee.Or(), Expressions = \
					[ee.NAryOperatorExpression(ee.And(), Expressions = [RightExpression(j,
						length)] + [_EvaluationExpression(LeftExpression, n)
							for n in xrange(position, j)]) for j in
								xrange(position, length)])
		return ee.NAryOperatorExpression(ee.Or(), Expressions = \
				[ee.NAryOperatorExpression(ee.And(), Expressions = \
				[_EvaluationExpression(RightExpression, j)] + \
				[_EvaluationExpression(LeftExpression, n) for n in xrange(position, j)]) for j in xrange(position, length)])

class Release(le.Release, CachedCall):
	def _cached(self, LeftExpression, RightExpression, position = 0, length =
			0):
		if _ltl_expression(LeftExpression) and \
				_ltl_expression(RightExpression):
			return ee.NAryOperatorExpression(ee.Or(), Expressions = \
				[ee.NAryOperatorExpression(ee.And(), Expressions = [LeftExpression(j, length)] + \
					[RightExpression(n, length) for n in xrange(position, j)]) for j in xrange(position, length)])
		if _ltl_expression(LeftExpression):
			return ee.NAryOperatorExpression(ee.Or(), Expressions = \
					[ee.NAryOperatorExpression(ee.And(), Expressions = [LeftExpression(j,
						length)] + [_EvaluationExpression(RightExpression, n)
							for n in xrange(position, j)]) for j in
						xrange(position, length)])
		if _ltl_expression(RightExpression):
			return ee.NAryOperatorExpression(ee.Or(), Expressions = \
					[ee.NAryOperatorExpression(ee.And(), Expressions = \
						[_EvaluationExpression(LeftExpression, j)] + [RightExpression(n, length) for n in xrange(position, j)])
							for j in xrange(position, length)])
		return ee.NAryOperatorExpression(ee.Or(), Expressions = \
				[ee.NAryOperatorExpression(ee.And(), Expressions = \
					[_EvaluationExpression(LeftExpression, j)] + [EvaluationExpression(RightExpression, n) for n in xrange(position, j)])
						for j in xrange(position, length)])

# these classes define the __call__ method of LTL Expressions for the bounded
# semantics evaluation. Each __call__ method should in turn produce an
# ExpressionEvaluation instance with appropriate operator. The result of the
# expansion may be evaluated on a data object by a result(data) call

class LTLUnaryOperatorExpression(le.LTLUnaryOperatorExpression):
	def __call__(self, position = 0, length = 0):
		return self.Operator(self.Expression, position, length)

class LTLNAryOperatorExpression(le.LTLNAryOperatorExpression):
	def __call__(self, position = 0, length = 0):
		return self.Operator(self.Expressions, position, length)

class LTLBinaryOperatorExpression(le.LTLBinaryOperatorExpression):
	def __call__(self, position = 0, length = 0):
		return self.Operator(self.LeftExpression, self.RightExpression,
				position, length)

class EvaluationExpression(ee.Expression, object):
	# terminates the chain of position evaluation to remember data index to
	# call
	cache = {}
	@classmethod
	def key(*args, **kwargs):
		return hash(repr(args) + repr(kwargs))
	def callKey(self, data):
		return hash(repr(data)) + self.callHash
	def __init__(self, Expression, position = 0, length = 0):
		self.position = position
		self.length = length
		self.Expression = Expression
		self.callHash = hash(repr(Expression) + repr(length) + repr(position))
		logger.debug("EvaluationExpression: init: %s, %s, %s" % (str(Expression), position, length))
	def __call__(self, data):
		# assuming data is sufficiently small 2*|AP|
		key = self.callKey(data)
		if key in EvaluationExpression.cache:
			return EvaluationExpression.cache[key]
		logger.debug("EvaluationExpression: call: %s(%s)" % (str(self.Expression), data[..., self.position]))
		EvaluationExpression.cache[key] = self.Expression(data[...,self.position])
		return EvaluationExpression.cache[key]
	def __repr__(self):
		return "(%s: %s)" % (str(self.Expression), self.position)

def _EvaluationExpression(Expression, position, length=0):
	key = EvaluationExpression.key(Expression, position, length)
	if key in EvaluationExpression.cache:
		logger.debug("EvaluationExpression: hit: %s" % key)
		ret = EvaluationExpression.cache[key]
	else:
		ret = EvaluationExpression.cache[key] = \
		       EvaluationExpression(Expression, position, length)
	return ret

class X:
	def __repr__(self):
		return "X"

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	data = np.array([1, 2, 3, 4, 5, 6, 7])
	F = Finally()
	gt = ee.Greater()
	x = X()
	n = ee.NameAtom(x)
	v = ee.ValueAtom(5)
	ne = ee.AtomExpression(n)
	ve = ee.AtomExpression(v)
	gte = ee.BinaryOperatorExpression(gt, ne, ve)

	ex = LTLUnaryOperatorExpression(F, gte)
	print "The expression: %s" % str(ex)
	ev = ex(0, 7)
	print "The expression expanded: %s" % str(ev)
	print "Evaluation on data: %s" % str(ev(data))
	# (x <= 3) U (x >= 4)
	# ((x <=3) U (x >=4)) U (x >=6)
	va0 = ee.ValueAtom(3)
	va1 = ee.ValueAtom(4)
	va2 = ee.ValueAtom(6)
	vae0 = ee.AtomExpression(va0)
	vae1 = ee.AtomExpression(va1)
	vae2 = ee.AtomExpression(va2)
	be0 = ee.BinaryOperatorExpression(ee.LowerEqual(), ne, vae0)
	be1 = ee.BinaryOperatorExpression(ee.GreaterEqual(), ne, vae1)
	be2 = LTLBinaryOperatorExpression(Until(), be0, be1)
	be3 = ee.BinaryOperatorExpression(ee.GreaterEqual(), ne, vae2)
	be4 = LTLBinaryOperatorExpression(Until(), be2, be3)
	# (x <= 3) U (x >= 4)
	#print be2
	#expanded = be2(0, 7)
	#print expanded
	#print expanded(data)
	# ((x <=3) U (x >=4)) U (x >=6)
	print be4
	expanded = be4(0, 7)
	print expanded
	print expanded(data)
	print expanded.cahce.items().length
	# a complex example: (x > 2) R (X (x == 3) && F (x > 5))
#	va0 = ee.ValueAtom(2)
#	va1 = ee.ValueAtom(3)
#	va2 = ee.ValueAtom(5)
#	vae0 = ee.AtomExpression(va0)
#	vae1 = ee.AtomExpression(va1)
#	vae2 = ee.AtomExpression(va2)
#	be0 = ee.BinaryOperatorExpression(ee.Greater(), ne, vae0)
#	be1 = ee.BinaryOperatorExpression(ee.Equal(), ne, vae1)
#	be2 = ee.BinaryOperatorExpression(ee.Greater(), ne, vae2)
#	ue0 = LTLUnaryOperatorExpression(Next(), be1)
#	ue1 = LTLUnaryOperatorExpression(Finally(), be2)
#	ne0 = LTLNAryOperatorExpression(And(), [ue0, ue1])
#	be3 = LTLBinaryOperatorExpression(Release(), be0, ne0)
#	print "Another expression: %s" % str(be3)
#	ev = be3(0, 7)
#	print "Another expression expanded: %s" % str(ev)
#	print "Another expanded expression evaluated on data: %s: %s" % (data,
#			str(ev(data)))
#
#
