#!--*--coding:utf-8--*--

import pygame as pyg
from form import Form

class Zone:

	def __init__(self, color, position, size, authorized = True):
		self.size = size
		self.position = position
		self.authorized = authorized
		self.surface = pyg.Surface((size[0], size[1]))
		self.surface.fill(color)
		self.rect = self.surface.get_rect()
		self.rect.x, self.rect.y = position[0], position[1]

	def isOn(self, graphform):
		on = True
		rectX = graphform.formeRect.x
		rectY = graphform.formeRect.y
		for sommet in graphform.forme.get_sommets(graphform.forme.new_scale):
			p = [sommet[0] + rectX, sommet[1] + rectY]
			on &= self.rect.collidepoint(p)
		return on