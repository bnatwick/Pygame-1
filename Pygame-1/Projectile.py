#Projectile class

import pygame

class projectile:
	def __init__(self, x, y, direction, velocity, radius=5, color=(0,0,0)):
		self.x = x
		self.y = y
		self.direction = direction
		self.velocity = velocity
		self.radius = radius
		self.color = color

	def draw(self,surface):
		pygame.draw.circle(surface,self.color,(self.x,int(self.y)), self.radius)
