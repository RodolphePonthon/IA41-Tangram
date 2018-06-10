#!--*--coding:utf-8--*--

import pygame as pyg

class Button:

	def __init__(self, position, size, texture):
		self.size = size
		self.position = position
		self.surface = pyg.image.load(texture)
		self.surface = pyg.transform.scale(self.surface, (int(size[0]), int(size[1])))
		self.rect = self.surface.get_rect()
		self.rect.x, self.rect.y = position[0], position[1]

	def isOn(self, p):
		return self.rect.collidepoint(p)