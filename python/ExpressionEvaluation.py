#!/usr/bin/env python
# provides a "standard" (numpy) evaluation of Expression Structures
import ExpressionStructure as ex
import logging
import math
from Cached import CachedCall, CachedNew
logger = logging.getLogger(__name__)

# --- ATOMS

class NameAtom(ex.NameAtom):
	# name evaluation for a data object
	def __call__(self, data=None):
		# data is "queried" for self.Contents and its value is returned
		logger.debug("NameAtom: call: data: %s" % str(data))
		if not data:
			return data
		try:
			ret = data[self.Contents]
			logger.debug("data[%s] -> %s" % (str(self.Contents), str(ret)))
		except:
			try:
				ret = getattr(data, self.Contents)
				logger.debug("getattr(data, %s) -> %s" % (str(self.Contents), str(ret)))
			except:
				# last chance to retrieve ;)
				ret = data
				logger.debug("data -> %s" % str(ret))
		return ret

class ValueAtom(ex.ValueAtom):
	# value "evaluation" for a data object
	def __call__(self, data=None):
		# silently ignore data and return self.Contents instead
		return self.Contents

class TrueAtom(ex.TrueAtom):
	# true "evaluation" for a data object
	def __call__(self, data=None):
		# silently ignore data and return True instead
		return True

class FalseAtom(ex.FalseAtom):
	# false "evaluation" for a data object
	def __call__(self, data=None):
		# silently ignore data and return False instead
		return False

# --- OPERATORS

class Plus(ex.Plus):
	# plus evaluation for its call method arguments
	def __call__(self, *args):
		# return a sum of args
		return reduce(lambda x, y: x + y, args)

class Times(ex.Times):
	# times evaluation for its call method arguments
	def __call__(self, *args):
		# return a product of args
		return reduce(lambda x, y: x * y, args)

class Power(ex.Power):
	# power evaluation for its call method arguments
	def __call__(self, a, b):
		return math.pow(a, b)

class Or(ex.Or):
	# or evaluation for its call method arguments
	def __call__(self, *args):
		return reduce(lambda x, y: x or y, args)

class And(ex.And):
	# and evaluation for its call method arguments
	def __call__(self, *args):
		return reduce(lambda x, y: x and y, args)

class Not(ex.Not):
	# "not" evaluation for its call method argument
	def __call__(self, a):
		return not a

class Greater(ex.Greater):
	def __call__(self, a, b):
		return a > b

class Lower(ex.Lower):
	def __call__(self, a, b):
		return a < b

class GreaterEqual(ex.GreaterEqual):
	def __call__(self, a, b):
		return a >= b

class LowerEqual(ex.LowerEqual):
	def __call__(self, a, b):
		return a <= b

class Equal(ex.Equal):
	def __call__(self, a, b):
		return a == b

class NotEqual(ex.NotEqual):
	def __call__(self, a, b):
		return a != b

# --- OPERATOR EXPRESSION TYPES

class Expression(ex.Expression):
	# "abstract" expression evaluation type
	def __call__(self, data):
		# abstract method to be overriden by subtypes
		pass

class BinaryOperatorExpression(ex.BinaryOperatorExpression):
	# binary operator evaluation for data
	def __call__(self, data):
		# apply self.Operator to SubExpressions evaluated on data
		return self.Operator(self.LeftExpression(data), self.RightExpression(data))

class NAryOperatorExpression(ex.NAryOperatorExpression):
	# NAry operator evaluation for data
	def __call__(self, data):
		# apply self.Operator to SubExpressions evaluated on data
		# print type(self.Expressions)
		logger.debug("NAryOperatorExpression: call: operator: %s, expressions: %s" % \
				(str(self.Operator), str(self.Expressions)))
		return reduce(self.Operator, map(lambda x: x(data), self.Expressions))

class UnaryOperatorExpression(ex.UnaryOperatorExpression):
	# Unary operator evaluation for data
	def __call__(self, data):
		return self.Operator(self.Expression(data))

# --- ATOM EXPRESSION TYPE

class AtomExpression(ex.AtomExpression):
	# evaluation of data
	def __call__(self, data):
		# return atom value on data
		return self.Atom(data)

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	n1 = NameAtom("milan")
	data = {"milan":1}
	milan = NameAtom(-1)
	print n1(data)
	dataM = [1,2,3,4,5]
	print milan(dataM)
	class DataO:
		milan = 3
	dataO = DataO()
	print n1(dataO)
	v1 = ValueAtom("milan")
	print v1(dataO)
	print v1(data)
	print v1(dataM)
	p = Plus()
	print p(dataM, [1], [2, 3])
	t = Times()
	print t(dataM, 2)
	w = Power()
	print w(2, 3)
	n = Not()
	print n(True)

	# a complex example ;)
	n1=NameAtom("milan")
	v1=ValueAtom(3.141592654)
	v2=ValueAtom(1.0)
	ae1 = AtomExpression(n1)
	ae2 = AtomExpression(v1)
	ae3 = AtomExpression(v2)
	ge = GreaterEqual()
	anOr = Or()
	t = TrueAtom()
	ne = NotEqual()

	boe1 = BinaryOperatorExpression (w, ae1, ae2)
	boe2 = BinaryOperatorExpression (ge, ae1, ae2)
	boe3 = BinaryOperatorExpression (ne, boe1, ae3)
	noe1 = NAryOperatorExpression (anOr, Expressions = [t, boe3, boe2])
	uoe1 = UnaryOperatorExpression (n, noe1)
	print "A complex example structure:"
	print uoe1
	print "A complex example evaluation on data: %s" % data
	print uoe1(data)
