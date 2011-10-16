#!/usr/bin/env python
# stolen from: http://openopt.org/FuncDesignerDoc#Solving_ODE
# utilizes the openopt soft: openopt.org
# Initial conditions evaluation of a
# Bayramov oscilator
#
from FuncDesigner import *
from numpy import arange

# variables
x, y, z, t = oovars('x', 'y', 'z', 't')
bayramov = {
		x: 0.0005 - 250.1*x, # dx/dt
		y: 0.0001 - 0.1*y + 252.1*x*y + 301.1*y*z, # dy/dt
		z: 253.1*x*y  - 340.1*y*z # dz/dt
#		x: 2*x + cos(3*y-2*z) + exp(5-2*t), # dx/dt
#		y: arcsin(t/5) + 2*x + sinh(2**(-4*t)) + (2+t+sin(z))**(1e-1*(t-sin(x)+cos(y))), # dy/dt
#		z: x + 4*y - 45 - sin(100*t) # dz/dt
		}

i0 = {
		x: 0.0015,
		y: 0.00095,
		z: 0.00038
		}

tarray = arange(0.0, 960.0, 0.1)
bayramovODE = ode(bayramov, i0, t, tarray)
bayramovResult = bayramovODE.solve(solver="interalg", ftol=0.05)
X, Y, Z = bayramovResult(x, y, z)
print (Z, Y, Z)
print bayramovResult.msg
