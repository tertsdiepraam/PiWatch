"""This file provides the text classes for PiWatch-apps."""
import pygame
from .drawable import *

import os	

class ImageAttrs(AttrSet):
	def setDefaults(self):
		super().setDefaults()
		self.attrs.update({
			'filename': None,
			'size_x': None,
			'size_y': None})
	
class Image(PiDrawable):
	DEFAULTATTRS = ImageAttrs
	
	def setup(self, parent):
		self.parent = parent
		self.imagefile = pygame.image.load(self.filename)
		self.image = pygame.image.load(self.filename)
		self.rect = self.image.get_rect()
		self.set_size()
		self.set_pos()
	
	def set_size(self):
		if self.size_x and not self.size_y:
			size_x = self.size_x
			size_y = int(self.size_x * self.rect.height / self.rect.width)
		elif self.size_y and not self.size_x:
			size_x = int(self.size_y * self.rect.width / self.rect.height)
			size_y = self.size_y
		else:
			size_x = self.size_x
			size_y = self.size_y
		self.image = pygame.transform.scale(self.imagefile, (size_x, size_y))
		self.rect = self.image.get_rect()
	
	def update(self, filename=None):
		if filename:
			self.filename = filename
			self.image = pygame.image.load(self.filename)
		self.set_size()
		self.set_pos()