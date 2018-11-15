"""Fichier contenant le code implémentant un moteur physique basique ainsi qu'une modélisation simpliste de fusée"""

# -*-coding:utf-8-*

__author__ = 'Sofa'
__copyright__ = 'Copyright 2018, Sofa'
__license__ = 'GPL'

import matplotlib.pyplot as plt

from math import sqrt, exp

g = 9.81


class Vect2D:

	def __init__(self, x=0.0, y=0.0):

		self.x = x
		self.y = y

	def dot(self, vect):
		return self.x * vect.x + self.y + vect.y

	def __add__(self, other):

		self.x += other.x
		self.y += other.y
		return self.copy()

	def __sub__(self, other):

		self.x -= other.x
		self.y -= other.y
		return self.copy()

	def __mul__(self, other):

		if type(other) is int or type(other) is float:

			self.x *= other
			self.y *= other
			return self.copy()

		else:
			raise Exception("Multiplying vectors")

	def __rmul__(self, other):
		self.__mul__(other)
		return self.copy()

	def __truediv__(self, other):
		self.__mul__(1/other)
		return self.copy()

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def norme(self):
		return sqrt(pow(self.x, 2) + pow(self.y, 2))

	def unit(self):
		if self.x == 0 and self.y == 0:
			return Vect2D()  # si le vecteur est nul on retourne le vecteur nul
		return Vect2D(self.x / self.norme(), self.y / self.norme())

	def __copy__(self):
		return Vect2D(self.x, self.y)

	def copy(self):
		return self.__copy__()

	def __str__(self):
		return "<{0}, {1}>".format(self.x, self.y)


class PhysObj:

	def __init__(self):

		self.mass = 0
		self.vitesse = Vect2D()
		self.pos = Vect2D()
		self.acceleration = Vect2D()

	def update(self, dt=0.1):

		self.vitesse += self.acceleration.copy() * dt
		self.pos += self.vitesse.copy() * dt
		self.acceleration = Vect2D()


class Fusee(PhysObj):

	def __init__(self):

		PhysObj.__init__(self)
		self.dm = 15e3  # saturn V
		self.ve_gaz = 2500  # wikipedia tuyères

		self.masse_vide = 130e3
		self.masse_carburant = 2700e3
		self.mass = self.masse_vide + self.masse_carburant

	def update(self, dt=0.1):

		Cx = 0.05
		rho = calcul_rho(self.pos.y)

		S = 12  # surface en m-2 de la tuyère
		dp = 70  # différence de pression entre le gaz sortant de la tuyère et l'atm

		if self.masse_carburant >= 0:

			self.masse_carburant -= self.dm * dt
			self.mass = self.masse_carburant + self.masse_vide

			poussee = self.dm * self.ve_gaz

			self.acceleration = Vect2D(0, poussee)

		v = self.vitesse.norme()

		R = 1/2 * Cx * rho * v
		a = 1

		self.acceleration -= R*self.vitesse.unit()

		self.acceleration -= Vect2D(0, g * self.mass)

		self.acceleration /= self.mass
		PhysObj.update(self)


def calcul_rho(z):
	R = 8.31
	T = 300
	M = 29e-3

	return exp(-z*M*g/R*T)


t_tot = 200
dt = 0.001

step = int(t_tot / dt)

f = Fusee()

t = list()
y = list()
v = list()

t_ecoule = 0
for i in range(step):
	if step % 1 == 0:
		t.append(t_ecoule)
		y.append(f.pos.y)
		v.append(f.vitesse.norme())

	f.update(dt)

	t_ecoule += dt
plt.plot(t, y)
# plt.plot(t, v)
plt.show()
