#!/usr/bin/env python
from numpy import *
from scipy import integrate

class LotkaVolterra2D(object):
	"""
	stolen from: http://www.scipy.org/Cookbook/LoktaVolterraTutorial
	"""
	def __init__(self, X0, time, a=10.1, b=1.5, c=1.5, d=0.75):
		self.a = a
		self.b = b
		self.c = c
		self.d = d
		self.time = time
		self.X0 = X0
		self.result, self.message = integrate.odeint(self.dX_dt, self.X0,
				self.time, full_output=True)
	def dX_dt(self, X, t=0):
		"""growth-rate of the population"""
		return array([self.a*X[0] - self.b*X[0]*X[1], -self.c*X[1] + self.b*self.d*X[0]*X[1]])
	def d2X_dt2(self, X, t=0):
		"Jacobian Matrix"
		return array([[self.a -self.b*X[1], -self.b*X[0]], [self.b*self.d*X[1], -self.c + self.b*self.d*X[0]]])


if __name__ == "__main__":
	startPoint = array([10, 5])
	timeArray = linspace(0, 15, 1000)
	lv = LotkaVolterra2D(startPoint, timeArray)
	print lv.result
