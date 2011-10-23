#!/usr/bin/env python
# abstract Expression structure description
# all __str__ methods dump in almost a pythonic syntax to make the output more readable
# all __repr__ methods dump in "constructor" syntax

from abc import ABCMeta
from collections import namedtuple

# a hook for iterables assertion checking
class _Iterable:
	__metaclass__ = ABCMeta

_Iterable.register(list)
_Iterable.register(tuple)
_Iterable.register(dict)

# ATOM TYPE

class Atom:
	# to denote something is an Atom type
	__metaclass__ = ABCMeta

	def __repr__(self):
		return "Atom()"

# ATOM TYPES
# ID TYPE

class NameAtom(namedtuple('Name', 'Contents'), Atom):
	# to denote something is a Name Atom type

	def __str__(self):
		return str(self.Contents)

class TrueAtom(Atom):
	# to denote something is a True Atom type
	# Borg
	__shared_state = {}

	def __repr__(self):
		return "True()"

	def __str__(self):
		return "True"

	def __init__(self):
		self.__dict__ = self.__shared_state

class FalseAtom(Atom):
	# to denote something is a False Atom type
	# Borg
	__shared_state = {}

	def __repr__(self):
		return "False()"

	def __str__(self):
		return "False"

	def __init__(self):
		self.__dict__ = self.__shared_state

class ValueAtom(namedtuple('Value', 'Contents'), Atom):
	# to denote something is a Value Atom type

	def __str__(self):
		return str(self.Contents)

# OPERATOR TYPES
# Borg

class NAry:
	# to denote something is an NAry object
	# Borg
	__metaclass__ = ABCMeta
	__shared_state = {}
	def __repr__(self):
		return "NAry()"
	
	def __init__(self):
		self.__dict__ = self.__shared_state


class Binary(NAry):
	# to denote something is a Binary object
	# Borg
	def __repr__(self):
		return "Binary()"

class Unary(NAry):
	# to denote something is an Unary object
	# Borg
	def __repr__(self):
		return "Unary()"

class Operator:
	# to denote something is an Operator
	# Borg
	__metaclass__ = ABCMeta
	__shared_state = {}

	def __repr__(self):
		return "Operator()"

	def __init__(self):
		self.__dict__ = self.__shared_state

class Plus(NAry, Operator):
	# the Plus atom is an NAry Operator in mathml
	def __repr__(self):
		return "Plus()"

	def __str__(self):
		return "+"

class Times(NAry, Operator):
	# the Times atom is an NAry Operator in mathml
	def __repr__(self):
		return "Times()"

	def __str__(self):
		return "*"

class Power(Binary, Operator):
	# the Power atom is a Binary Operator in mathml
	def __repr__(self):
		return "Power()"

	def __str__(self):
		return "exp"

class Mod(Binary, Operator):
	# the Mod is a Binary Operator in mathml
	def __repr__(self):
		return "Mod()"

	def __str__(self):
		return "%"

class Or(NAry, Operator):
	def __repr__(self):
		return "Or()"

	def __str__(self):
		return "or"

class And(NAry, Operator):
	def __repr__(self):
		return "And()"

	def __str__(self):
		return "and"

class Xor(NAry, Operator):
	def __repr__(self):
		return "Xor()"

	def __str__(self):
		return "xor"


class Not(Unary, Operator):
	def __repr__(self):
		return "Not()"

	def __str__(self):
		return "not"

class Greater(Binary, Operator):
	def __repr__(self):
		return "Greater()"

	def __str__(self):
		return ">"

class Lower(Binary, Operator):
	def __repr__(self):
		return "Lower()"

	def __str__(self):
		return "<"

class GreaterEqual(Binary, Operator):
	def __repr__(self):
		return "GreaterEqual()"

	def __str__(self):
		return ">="

class LowerEqual(Binary, Operator):
	def __repr__(self):
		return "LowerEqual()"

	def __str__(self):
		return "<="

class Equal(Binary, Operator):
	def __repr__(self):
		return "Equal()"

	def __str__(self):
		return "=="

class NotEqual(Binary, Operator):
	def __repr__(self):
		return "NotEqual()"

	def __str__(self):
		return "!="

# EXPRESSION TYPE

class Expression:
	# to denote something is an Expression object
	__metaclass__ = ABCMeta

	def __repr__(self):
		return "Expression()"

# OPERATOR EXPRESSION TYPES

class BinaryOperatorExpression(
	namedtuple('BinaryOperatorExpression', 'Operator LeftExpression RightExpression'),
	Expression):
	# specialized Binary Expression type

	def __init__ (self, anOperator, LeftExpression, RightExpression):
		# checking, etc
		assert isinstance(anOperator, Binary)
		assert isinstance(anOperator, Operator)
		assert isinstance(LeftExpression, Expression)
		assert isinstance(RightExpression, Expression)

	def __str__(self):
		return "(" + str(self.LeftExpression) + " " + str(self.Operator) + " " + str(self.RightExpression) + ")"

class NAryOperatorExpression(Expression):
	# specialized NAry Expression type

	def __init__(self, anOperator, *args):
		# checking, etc
		assert isinstance(anOperator, NAry)
		assert not isinstance(anOperator, Unary)
		assert not isinstance(anOperator, Binary)
		self.Expressions = args
		self.Operator = anOperator

	def __str__(self):
		return "(" + str(self.Operator) + " " + \
		" ".join(map(str, self.Expressions)) + ")"

class UnaryOperatorExpression(
	namedtuple('UnaryOperatorExpression', 'Operator, Expression'),
	Expression):
	# specialized unary Operator Expression type

	def __init__ (self, anOperator, anExpression):
		# checking, etc
		assert isinstance(anOperator, Unary)
		assert isinstance(anOperator, Operator)
		assert isinstance(anExpression, Expression)

	def __str__ (self):
		return "(" + str(self.Operator) + " " + str(self.Expression) + ")"

# ATOM EXPRESSION TYPE

class AtomExpression(
	namedtuple('AtomExpression', 'Atom'),
	Expression):
	# specialized ID Expression type

	def __init__ (self, anAtom):
		# checking, etc
		assert isinstance(anAtom, Atom)

	def __str__(self):
		return str(self.Atom)

if __name__ == "__main__":
	p=Power()
	e=Expression()
	boe = BinaryOperatorExpression(p, e, e)
	print boe
	n = Not()
	uoe = UnaryOperatorExpression(n, e)
	print uoe
	aPlus=Plus()
	noe = NAryOperatorExpression(aPlus, [uoe, boe])
	print str(noe)

	# a complex example ;)
	n1=NameAtom("milan")
	v1=ValueAtom("3.141592654")
	v2=ValueAtom("1.0f")
	ae1 = AtomExpression(n1)
	ae2 = AtomExpression(v1)
	ae3 = AtomExpression(v2)
	ge = GreaterEqual()
	anOr = Or()
	t = TrueAtom()
	ne = NotEqual()

	boe1 = BinaryOperatorExpression (p, ae1, ae2)
	boe2 = BinaryOperatorExpression (ge, ae1, ae2)
	boe3 = BinaryOperatorExpression (ne, boe1, ae3)
	noe1 = NAryOperatorExpression ( anOr, [t, boe3, boe2])
	uoe1 = UnaryOperatorExpression (n, noe1)
	print "A complex example:"
	print uoe1
