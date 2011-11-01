#!/usr/bin/env python
# provides Acyclic Symbolic Bounded Evaluation to LTLExpression structures
import LTLExpression as le
import ExpressionEvaluation as ee
import ExpressionStructure as ex
import numpy as np
import itertools as it
import logging, os

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

class And(le.And):
	def __call__(self, Expressions, position = 0, length = 0):
		ltl_expressions, other_expressions = _split_expressions(Expressions)
		return ee.NAryOperatorExpression(ee.And(), Expressions = map(lambda x: x(position,
			length), ltl_expressions) + map(lambda x: EvaluationExpression(x,
				position), other_expressions))

class Or(le.Or):
	def __call__(self, Expressions, position = 0, length = 0):
		ltl_expressions, other_expressions = _split_expressions(Expressions)
		return ee.NAryOperatorExpression(ee.Or(), Expressions = map(lambda x: x(position,
			length), ltl_expressions) + map(lambda x: EvaluationExpression(x,
				position), other_expressions))

class Not(le.Not):
	def __call__(self, Expression, position = 0, length = 0):
		if _ltl_expression(Expression):
			return ee.UnaryOperatorExpression(ee.Not(), Expression(position,
				length))
		return  ee.UnaryOperatorExpression(ee.Not(), EvaluationExpression(
			Expression, position))

class Next(le.Next):
	def __call__(self, Expression, position = 0, length = 0):
		if position >= length:
			# return "False" if on end
			return ee.AtomExpression(ee.FalseAtom())
		if _ltl_expression(Expression):
			return Expression(position + 1, length)
		return EvaluationExpression(Expression, position)

class Globally(le.Globally):
	def __call__(self, Expression, position = 0, length = 0):
		# Globally always "False" on acyclic trajectories
		return ee.AtomExpression(ee.FalseAtom())

class Finally(le.Finally):
	def __call__(self, Expression, position = 0, length = 0):
		if _ltl_expression(Expression):
			logger.debug("Finally: LTL expansion")
			return ee.NAryOperatorExpression(ee.Or(), Expressions = [ Expression(x, length)
				for x in xrange(position, length)])
		logger.debug("Finally: non-LTL expansion: %s" % str(Expression))
		return ee.NAryOperatorExpression(ee.Or(), Expressions = [ EvaluationExpression(Expression,
			x) for x in xrange(position, length)])

class Until(le.Until):
	def __call__(self, LeftExpression, RightExpression, position = 0, length =
			0):
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
							[EvaluationExpression(RightExpression, j)] +
						[LeftExpression(n, length) for n in xrange(position, j)])
							for j in xrange(position, length)])
		if _ltl_expression(RightExpression):
			return ee.NAryOperatorExpression(ee.Or(), Expressions = \
					[ee.NAryOperatorExpression(ee.And(), Expressions = [RightExpression(j,
						length)] + [EvaluationExpression(LeftExpression, n)
							for n in xrange(position, j)]) for j in
								xrange(position, length)])

class Release(le.Release):
	def __call__(self, LeftExpression, RightExpression, position = 0, length =
			0):
		if _ltl_expression(LeftExpression) and \
				_ltl_expression(RightExpression):
			return ee.NAryOperatorExpression(ee.Or(), Expressions = \
				[ee.NAryOperatorExpression(ee.And(), Expressions = [LeftExpression(j, length)] + \
					[RightExpression(n, length) for n in xrange(position, j)]) for j in xrange(position, length)])
		if _ltl_expression(LeftExpression):
			return ee.NAryOperatorExpression(ee.Or(), Expressions = \
					[ee.NAryOperatorExpression(ee.And(), Expressions = [LeftExpression(j,
						length)] + [EvaluationExpression(RightExpression, n)
							for n in xrange(position, j)]) for j in
						xrange(position, length)])
		if _ltl_expression(RightExpression):
			return ee.NAryOperatorExpression(ee.Or(), Expressions = \
					[ee.NAryOperatorExpression(ee.And(), Expressions = \
						[EvaluationExpression(LeftExpression, j)] + [RightExpression(n, length) for n in xrange(position, j)])
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

class EvaluationExpression(ee.Expression):
	# terminates the chain of position evaluation to remember data index to
	# call
	def __init__(self, Expression, position = 0, length = 0):
		logger.debug("EvaluationExpression: init: %s, %s, %s" % (str(Expression), position,
			length))
		self.position = position
		self.length = length
		self.Expression = Expression
	def __call__(self, data):
		logger.debug("EvaluationExpression: call: %s(%s)" % (str(self.Expression),
			data[...,self.position]))
		return self.Expression(data[...,self.position])
	def __repr__(self):
		return "(%s: %s)" % (str(self.Expression), self.position)

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
	v = ee.ValueAtom(8)
	ne = ee.AtomExpression(n)
	ve = ee.AtomExpression(v)
	gte = ee.BinaryOperatorExpression(gt, ne, ve)

	ex = LTLUnaryOperatorExpression(F, gte)
	print "The expression: %s" % str(ex)
	ev = ex(0, 7)
	print "The expression expanded: %s" % str(ev)
	print "Evaluation on data: %s" % str(ev(data))

	# a complex example: (x > 2) R (X (x == 3) && F (x > 5))
	va0 = ee.ValueAtom(2)
	va1 = ee.ValueAtom(3)
	va2 = ee.ValueAtom(5)
	vae0 = ee.AtomExpression(va0)
	vae1 = ee.AtomExpression(va1)
	vae2 = ee.AtomExpression(va2)
	be0 = ee.BinaryOperatorExpression(ee.Greater(), ne, vae0)
	be1 = ee.BinaryOperatorExpression(ee.Equal(), ne, vae1)
	be2 = ee.BinaryOperatorExpression(ee.Greater(), ne, vae2)
	ue0 = LTLUnaryOperatorExpression(Next(), be1)
	ue1 = LTLUnaryOperatorExpression(Finally(), be2)
	ne0 = LTLNAryOperatorExpression(And(), [ue0, ue1])
	be3 = LTLBinaryOperatorExpression(Release(), be0, ne0)
	print "Another expression: %s" % str(be3)
	ev = be3(0, 7)
	print "Another expression expanded: %s" % str(ev)
	print "Another expanded expression evaluated on data: %s: %s" % (data,
			str(ev(data)))


