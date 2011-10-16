#!/usr/bin/env python
from numpy import *
from scipy import integrate

class Wilhelm2D(object):
	def __init__(self, X0, time):
		self.time = time
		self.X0 = X0
		self.result, self.message = integrate.odeint(self.dX_dt, self.X0,
				self.time, full_output=True)
	def dX_dt(self, X, t=0):
		return array([16*X[1] - X[0]*X[0] - X[0]*X[1] - 1.5,
				X[0]*X[0] - 8*X[1]])
	def d2X_dt2(self, X, t=0):
		return array([[-2*X[0] - X[1], 16 - X[0]],
				[2*X[0], -8]])

if __name__ == "__main__":
	import pylab
	startPoint = array([3.0, 3.0])
	timeArray = linspace(0, 20, 2000)
	wh = Wilhelm2D(startPoint, timeArray)
	print wh.result
	print wh.message
	pylab.plot(wh.result.T[1], wh.result.T[0], 'g.')
	pylab.show()

