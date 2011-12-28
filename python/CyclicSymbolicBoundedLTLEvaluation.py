#!/usr/bin/env python
# provides Cyclic Symbolic Bounded Evaluation to LTLExpression structures
import LTLExpression as le
import ExpressionEvaluation as ee
from ExpressionEvaluation import NAryOperatorExpression as NOE
from ExpressionEvaluation import UnaryOperatorExpression as UOE
from ExpressionEvaluation import BinaryOperatorExpression as BOE
import ExpressionStructure as ex
import numpy as np
import itertools as it
import logging, os

logger = logging.getLogger(__name__)

# The operators define the bounded Cyclic semantics for an LTL structure
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
	def __call__(self, Expressions, position = 0, length = 0, loop = 0):
		ltl_expressions, other_expressions = _split_expressions(Expressions)
		return NOE(ee.And(), Expressions = map(lambda x: x(position,
			length, loop), ltl_expressions) + map(lambda x: EvaluationExpression(x,
				position), other_expressions))

class Or(le.Or):
	def __call__(self, Expressions, position = 0, length = 0, loop = 0):
		ltl_expressions, other_expressions = _split_expressions(Expressions)
		return NOE(ee.Or(), Expressions = map(lambda x: x(position,
			length, loop), ltl_expressions) + map(lambda x: EvaluationExpression(x,
				position), other_expressions))

class Not(le.Not):
	def __call__(self, Expression, position = 0, length = 0, loop = 0):
		if _ltl_expression(Expression):
			return UOE(ee.Not(), Expression(position,
				length, loop))
		return  UOE(ee.Not(), EvaluationExpression(
			Expression, position))

class Next(le.Next):
	def __call__(self, Expression, position = 0, length = 0, loop = 0):
		if _ltl_expression(Expression):
			if i < loop:
				# before loop
				return Expression(i + 1, position, loop)
			else:
				# in loop
				return Expression(loop + ((position - loop + 1)%(length - loop)),
						length, loop)
		return EvaluationExpression(Expression, position)

class Globally(le.Globally):
	def __call__(self, Expression, position = 0, length = 0, loop = 0):
		if _ltl_expression(Expression):
			return NOE(ee.And(), Expressions = \
					[ Expression(j, length, loop) for j in xrange(
						min(position, loop), length)]
				)
		return NOE(ee.And(), Expressions = \
					[ EvaluationExpression(Expression, j) for j in xrange(
						min(position, loop), length)]
				)

class Finally(le.Finally):
	def __call__(self, Expression, position = 0, length = 0, loop = 0):
		if _ltl_expression(Expression):
			return NOE(ee.Or(), Expressions = \
					[ Expression(j, length, loop) for j in xrange(
						min(position, loop), length)]
				)
		return NOE(ee.Or(), Expressions = \
					[ EvaluationExpression(Expression, j) for j in xrange(
						min(position, loop), length)]
				)

# these classes define the __call__ method of LTL Expressions for the bounded
# semantics evaluation. Each __call__ method should in turn produce an
# ExpressionEvaluation instance with appropriate operator. The result of the
# expansion may be evaluated on a data object by a result(data) call

class LTLUnaryOperatorExpression(le.LTLUnaryOperatorExpression):
	def __call__(self, position = 0, length = 0, loop = 0):
		return self.Operator(self.Expression, position, length, loop)

class LTLNAryOperatorExpression(le.LTLNAryOperatorExpression):
	def __call__(self, position = 0, length = 0, loop = 0):
		return self.Operator(self.Expressions, position, length, loop)

class LTLBinaryOperatorExpression(le.LTLBinaryOperatorExpression):
	def __call__(self, position = 0, length = 0, loop = 0):
		return self.Operator(self.LeftExpression, self.RightExpression,
				position, length, loop)

class EvaluationExpression(ee.Expression):
	# terminates the chain of position evaluation to remember data index to
	# call
	def __init__(self, Expression, position = 0, length = 0, loop = 0):
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

def OscillationFactory(expression):
	# G((expression => F(!expression)) && (!expression => F(expression)))
	fp = LTLUnaryOperatorExpression(Finally(), expression)
	ne = LTLUnaryOperatorExpression(Not(), expression)
	fn = LTLUnaryOperatorExpression(Finally(), ne)
	oe1 = LTLNAryOperatorExpression(Or(), Expressions = [ne, fn])
	oe2 = LTLNAryOperatorExpression(Or(), Expressions = [expression, fp])
	ae = LTLNAryOperatorExpression(And(), Expressions = [oe1, oe2])
	return LTLUnaryOperatorExpression(Globally(), ae)

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	data = np.array([1, 2, 3, 4, 5, 6, 7])
	gt = ee.Greater()
	x = X()
	n = ee.NameAtom(x)
	v = ee.ValueAtom(3)
	ne = ee.AtomExpression(n)
	ve = ee.AtomExpression(v)
	gte = BOE(gt, ne, ve)
	oe = OscillationFactory(gte)
	print "The expression: %s" % str(oe)
	ev = oe(0, 7, 5)
	print "The expression expanded: %s" % str(ev)
	print "Evaluation on data: %s" % str(ev(data))
