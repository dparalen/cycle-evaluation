#!/usr/bin/env python
from numpy import *
from scipy import integrate

class Bayramov(object):
	def __init__(self, X0, time):
		self.time = time
		self.X0 = X0
		self.result, self.message = integrate.odeint(self.dX_dt, self.X0,
				self.time, full_output=True)
	def dX_dt(self, X, t=0):
		return array([0.0005 - 250*X[0]*X[1],
			0.0001 - 0.1*X[1] - 250*X[0]*X[1] + 300*X[1]*X[2],
			250*X[0]*X[1] - 300*X[1]*X[2]])
	def d2X_dt2(self, X, t=0):
		return array([
				[-250*X[1], -250*X[0], 0.],
				[-250*X[1], -0.1 -250*X[0] + 300*X[2], 300*X[1]],
				[250*X[1], 250*X[0] - 300*X[2], -300*X[1]]
			])

if __name__ == "__main__":
	import pylab as p
	import mpl_toolkits.mplot3d.axes3d as p3

	startPoint = array([0.0003, 0.0003, 0.006])
	timeArray = linspace(0, 960, 9600)
	ba = Bayramov(startPoint, timeArray)
	print ba.message
	fig = p.figure()
	ax = p3.Axes3D(fig)
	ax.plot3D(ba.result.T[0], ba.result.T[1], ba.result.T[2])
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')
	p.show()

