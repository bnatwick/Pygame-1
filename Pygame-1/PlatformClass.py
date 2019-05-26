#Platform Class

import pygame

class platform:
	def __init__(self,x,y,width,height,color):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color

	def draw(self, surface):
		pygame.draw.rect(surface,self.color,[self.x,self.y,self.width,self.height])

	def isContact(self,playerPosition,player):
		if (((self.x - player.width) <= playerPosition["x"] <= (self.x + self.width)) and 
			((self.y - player.height) <= playerPosition['y'] <= (self.y + self.height))):
			return True
		else:
			return False