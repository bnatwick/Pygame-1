#Spritesheet class

import pygame

class spriteSheet:
	def __init__(self, filename, cols, rows):
		self.sheet =pygame.image.load(filename)

		self.cols = cols
		self.rows = rows
		self.totalCellCount = cols * rows

		self.rect = self.sheet.get_rect()

		w = self.width = self.rect.width / cols
		h = self.height = self.rect.height / rows
		hw, hh = self.cellCenter = w/2, h/2

		self.cells = [(i % cols * w,i // cols * h, w, h) for i in range(self.totalCellCount)]
		self.handle = [(0,0),(-hw,0),(-w,0),
					   (0,-hh),(-hw,-hh),(-w,-hh),
					   (0,-h),(-hw,-h),(-w,-h)]

	def draw(self,surface,cellIndex,x,y,handle=0):
		surface.blit(self.sheet,(x + self.handle[handle][0],y + self.handle[handle][1]),self.cells[cellIndex])
