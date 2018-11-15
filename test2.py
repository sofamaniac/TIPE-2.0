# -*-coding:utf-8-*
__author__ = 'Sofa'
__copyright__ = 'Copyright 2018, Sofa'
__license__ = 'GPL'

import matplotlib.pyplot as plt
from math import exp
pos = 0
masse = 1
carburant = 2
dm = 3
ve = 4
vitesse = 5
acceleration = 6

g = 9.81

fusee = {pos: 0,
		 masse: 2700e3 + 130e3,
		 carburant: 2700e3,
		 dm: 15e3,
		 ve: 2500,
		 vitesse: 0,
		 acceleration: 0}


def calcul_acc(f, dt):

	f[acceleration] = 0

	if f[carburant] > 0:

		f[carburant] -= f[dm] * dt
		poussee = f[dm] * f[ve]

		f[acceleration] += poussee

	rho = calcul_rho(f[pos])
	Cx = 0.05
	R = 1 / 2 * Cx * rho

	f[acceleration] -= pow(f[vitesse], 2) * R

	f[acceleration] -= g * f[masse]

	f[acceleration] /= f[masse]


def calcul_rho(z):
	R = 8.31
	T = 300
	M = 29e-3

	return exp(-z*M*g/R*T)

t_exec = 600
dt = 0.1
steps = int(t_exec / dt)

yl = list()
tl = list()

t = 0

for i in range(steps):
	if fusee[pos] >= 0:

		calcul_acc(fusee, dt)
		fusee[vitesse] += fusee[acceleration] * dt
		fusee[pos] += fusee[vitesse] * dt

		yl.append(fusee[pos])
		tl.append(t)

		t += dt

plt.plot(tl, yl)
plt.show()


