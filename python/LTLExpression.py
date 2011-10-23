#!/usr/bin/env python
# an abstract LTL Expression representation
import ExpressionStructure
from ExpressionStructure import * 
from abc import *

class LTL:
	# base LTL type
	__metaclass__ = ABCMeta

# OPERATOR TYPES
class And(ExpressionStructure.And, LTL):
	def __invert__(self):
		return Or()

class Or(ExpressionStructure.Or, LTL):
	def __invert__(self):
		return And()

class Not(ExpressionStructure.Not, LTL):
	def __invert__(self):
		return None

class Next(Unary, Operator, LTL):
	# the Next Operator type

	def __repr__(self):
		return "Next()"

	def __str__(self):
		return "O"

	def __invert__(self):
		# ~X(Expression) == X(~Expression)
		return self

class Finally(Unary, Operator, LTL):
	# the Finally Operator type

	def __repr__(self):
		return "Finally()"

	def __str__(self):
		return "F"

class Globally(Unary, Operator, LTL):
	# the Globally Operator type

	def __repr__(self):
		return "Globally()"

	def __str__(self):
		return "G"

class Until(Binary, Operator, LTL):
	# the Until Oprerator type

	def __repr__(self):
		return "Until()"

	def __str__(self):
		return "U"

	def __invert__(self):
		return Release()

class Release(Binary, Operator, LTL):
	# the Release Operator Type

	def __repr__(self):
		return "Release()"

	def __str__(self):
		return "R"

	def __invert__(self):
		return Until()

# EXPRESSION TYPES

class LTLExpression(Expression, LTL):
	# LTL Expression type
	# an __iter__ should be implemented
	# stolen from http://docs.python.org/library/abc.html
	@abstractmethod
	def __iter__(self):
		# when implemented, __iter__ should return all the subexpressions
		# of an expression
		while False:
			yield None

	@abstractmethod
	def __invert__(self):
		# when implemented, __invert__ should return new inverted expression
		return None

	def get_iterator(self):
		return self.__iter__()

	def __eq__(self, other):
		assert isinstance(other, LTLExpression)
		return hash(self) == hash(other)

	def __ne__(self, other):
		return not(self.__eq__(self, other))

	def __hash__(self):
		return hash(str(self))

class LTLUnaryOperatorExpression(UnaryOperatorExpression, LTLExpression):
	# specific LTL Unary Operator Expression type

	def __init__(self, anOperator, anExpression):
		# checks, etc
		UnaryOperatorExpression.__init__(self, anOperator, anExpression)
		assert isinstance(anOperator, LTL)

	def __iter__(self):
		# recursive for LTL expressions
		if isinstance (self.Expression, LTL):
			for expr in self.Expression:
				yield expr
		else:
			yield self.Expression
		yield self

	def __invert__(self):
		# returns a new instance, inverted
		# recursive for LTL expressions
		if isinstance (self.Operator, Not):
			# ~~Expression == Expression
			return self.Expression
		elif isinstance (self.Operator, Next):
			# ~X(Expression) == X(~Expression)
			if isinstance (self.Expression, LTL):
				return LTLUnaryOperatorExpression(self.Operator, ~self.Expression)
			else:
				N = Not()
				return LTLUnaryOperatorExpression(self.Operator, \
					LTLUnaryOperatorExpression(N, self.Expression))

	def __hash__(self):
		return LTLExpression.__hash__(self)

	def __eq__(self, other):
		return LTLExpression.__eq__(self, other)

	def __ne__(self, other):
		return LTLExpression.__ne__(self, other)

class LTLBinaryOperatorExpression(BinaryOperatorExpression, LTLExpression):
	# specific LTL Binary Operator Expression type

	def __init__(self, anOperator, LeftExpression, RightExpression):
		# checks, etc
		BinaryOperatorExpression.__init__(self, anOperator, LeftExpression, RightExpression)
		assert isinstance(anOperator, LTL)

	def __iter__(self):
		# recursive for LTL expressions
		if isinstance (self.LeftExpression, LTL):
			for expr in self.LeftExpression:
				yield expr
		else:
			yield self.LeftExpression
		if isinstance (self.RightExpression, LTL):
			for expr in self.RightExpression:
				yield expr
		else:
			yield self.RightExpression

		yield self

	def __invert__(self):
		# returns a new instance, inverted
		# recursive for LTL expressions
		N = Not()
		# invert the sub-expressions first
		if isinstance (self.LeftExpression, LTL):
			lInv = ~self.LeftExpression
		else:
			lInv = LTLUnaryOperatorExpression(N, self.LeftExpression)

		if isinstance (self.RightExpression, LTL):
			rInv = ~self.RightExpression
		else:
			rInv = LTLUnaryOperatorExpression(N, self.RightExpression)
	
		# invert the operator and return
		return LTLBinaryOperatorExpression(~self.Operator, lInv, rInv)

	def __hash__(self):
		return LTLExpression.__hash__(self)

	def __eq__(self, other):
		return LTLExpression.__eq__(self, other)

	def __ne__(self, other):
		return LTLExpression.__ne__(self, other)

		

class LTLNAryOperatorExpression(NAryOperatorExpression, LTLExpression):
	# specific LTL NAry Operator Expression type
	# commutative

	def __init__(self, anOperator, Expressions):
		# checks, etc
		NAryOperatorExpression.__init__(self, anOperator, Expressions)
		assert isinstance(anOperator, LTL)

	def __iter__(self):
		# recursive for LTL expressions
		for expression in self.Expressions:
			if isinstance(expression, LTL):
				for expr in expression:
					yield expr
			else:
				yield expression
		yield self

	def __invert__(self):
		# returns a new instance, inverted
		# recursive for LTL expressions
		ExpressionsInv=[]
		N = Not()
		for Expression in self.Expressions:
			if isinstance(Expression, LTL):
				ExpressionsInv.append(~Expression)
			else:
				ExpressionsInv.append(LTLUnaryOperatorExpression(N, Expression))
		return LTLNAryOperatorExpression(~self.Operator, ExpressionsInv)

	def __hash__(self):
		# NAry operator expression is commutative
		return hash (str(self.Operator).join((sorted([ str(expr) for expr in self.Expressions ]))))

	def __eq__(self, other):
		return LTLExpression.__eq__(self, other)

	def __ne__(self, other):
		return LTLExpression.__ne__(self, other)

# TESTS
if __name__ == "__main__":
	n1 = NameAtom("milan")
	v1 = ValueAtom("42")
	aGreater = Greater()
	aGlobally = Globally()
	aFinally = Finally()
	en1 = AtomExpression (n1)
	ev1 = AtomExpression (v1)
	e1 = BinaryOperatorExpression (aGreater, en1, ev1)
	e2 = LTLUnaryOperatorExpression (aGlobally, e1)
	e3 = LTLUnaryOperatorExpression (aFinally, e2)
	print "e3: %s" % str(e3)
	print "All subformulas of e3:"
	for expr in e3:
		print "  " + str(expr)
	# print [ expr for expr in e3]
	X = Next()
	e4 = LTLUnaryOperatorExpression (X, e1)
	N = Not()
	e5 = LTLUnaryOperatorExpression (N, e4)
	print " e5: %s" % str(e5)
	# print [ expr for expr in e5 ]
	print "~e5: %s" % str(~e5)
	#print [ expr for expr in ~e5 ]
	e6 = LTLUnaryOperatorExpression (N, e1)
	e7 = LTLUnaryOperatorExpression (X, e6)
	print " e7: %s" % str(e7)
	print "~e7: %s" % str(~e7)
	print "All subformulas of ~e7:"
	for expr in ~e7:
		print "  " + str(expr)
	# ((True Until (milan > 42)) And (Not (Next (milan > 42))) Or (False))
	F_ = FalseAtom()
	T_ = TrueAtom()
	A = And()
	# print dir(A)
	O = Or()
	U = Until()
	ev2 = AtomExpression(T_)
	ev3 = AtomExpression(F_)
	e8 = LTLBinaryOperatorExpression(U, ev2, e1)
	e9 = LTLNAryOperatorExpression(A, [e8, e5])
	e10 = LTLNAryOperatorExpression(O, [e9, ev3]) 
	e01 = LTLNAryOperatorExpression(O, [ev3, e9])
	print "e10 == e01: %s" % (e10 == e01)
	print "set([e10]) == set([e01]): %s" % ( set([e10]) == set([e01]) )
	print "hash(e10): %s" % hash(e10)
	print "hash(e01): %s" % hash(e01)
	print "\nA slightly more complex example:"
	print " e10: %s" % str(e10)
	print "~e10: %s" % str(~e10)
	print "All subformulas of ~e10:"
	for expr in ~e10:
		print "  " + str(expr)
	print "e10 == ~e10: %s" % (e10 == ~e10)
	print type(~e10)
	print e10.__hash__()
	print "hash(~e10): %s" % (hash(~e10))
	print hash(e10.__str__())
	expressions = set([e10, ~e10, e7, ~e7])
	print [ hash(e) for e  in expressions ]
	print [ hash(e10), hash(~e10), hash(e7), hash(~e7)]
	print [ str(e) for e in expressions]
	e11 = ~e10
	print e11 in expressions
	print e11 in list(expressions)
	# print str(expressions)
