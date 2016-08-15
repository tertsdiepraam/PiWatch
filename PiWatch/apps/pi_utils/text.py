"""This file provides the text classes for PiWatch-apps."""
import pygame
from .drawable import *

import time

class TextAttrs(AttrSet):
	def setDefaults(self):
		super().setDefaults()
		self.attrs.update(
			{'size': 20,
			'color': (255,255,255),
			'font': 'Arial',
			'message': 'Example Text'})

class Text(PiDrawable):
	DEFAULTATTRS = TextAttrs()
	
	def setup(self, parent):
		"""Called when the app is opened"""
		self.parent = parent
		self.pyfont = pygame.font.SysFont(self.font, self.size)
		self.update()
		
	def update(self, message=None):
		if message:
			self.message = message
		if self.bg_color:
			self.image = self.pyfont.render(self.message, True, self.color, self.bg_color)
		else:
			self.image = self.pyfont.render(self.message, True, self.color)
		self.set_pos()

class ClockAttrs(TextAttrs):
	def setDefaults(self):
		super().setDefaults()
		self.attrs.update({
			'twentyfour': False})

class Clock(Text):
	DEFAULTATTRS = ClockAttrs()
		
	def update(self):
		"""Only called when the time has changed"""
		self.time = time.localtime()[3:5]
		hours = str(self.time[0]) if self.twentyfour else str(self.time[0]%12)
		minutes = str(self.time[1]) if len(str(self.time[1]))>1 else '0'+str(self.time[1])
		self.message = hours + ':' + minutes
		super().update()
	
	def draw(self, surface):
		"""Called every frame"""
		if self.time != time.localtime()[3:5]:
			self.update()
		super().draw(surface)

class TextCursor(Text): # just for testing. Provides a cursor when pygame.mouse.get_visible == False
	def set_pos(self):
		self.rect = self.image.get_rect()
		self.rect.center = pygame.mouse.get_pos()
		
	def draw(self, surface):
		self.set_pos()
		super().draw(surface)