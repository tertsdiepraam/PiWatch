"""This file provides the text classes for PiWatch-apps."""

import time

import pygame

from .drawable import *


class Text(PiDrawable):
    DEFAULTATTRS = dict(
        PiDrawable.DEFAULTATTRS,
        size=20,
        color=(255, 255, 255),
        font='yugothicyugothicuilight',
        message='Example Text'
    )

    def setup(self, parent):
        """Called when the app is opened"""
        self.parent = parent
        self.pyfont = pygame.font.SysFont(self.font, self.size)
        self.render_image()
        self.set_position()

    def render_image(self):
        if self.bg_color:
            self.image = self.pyfont.render(self.message, True, self.color, self.bg_color)
        else:
            self.image = self.pyfont.render(self.message, True, self.color)
        self.set_position()


class Clock(Text):
    DEFAULTATTRS = dict(
        Text.DEFAULTATTRS,
        twentyfour=False
    )

    def __init__(self, *attrs, **kwargs):
        super().__init__(*attrs, **kwargs)
        self.time = None

    def draw(self, surface):
        """Called every frame"""
        if self.time != time.localtime()[3:5]:
            self.time = time.localtime()[3:5]
            hours = str(self.time[0]) if self.twentyfour else str(self.time[0] % 12)
            minutes = str(self.time[1]) if len(str(self.time[1])) > 1 else '0' + str(self.time[1])
            self.update(message=hours+':'+minutes)
        super().draw(surface)


class TextCursor(Text):  # just for testing. Provides a cursor when pygame.mouse.get_visible == False
    def set_position(self):
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()

    def draw(self, surface):
        self.set_position()
        super().draw(surface)


class Date(Text):
    DEFAULTATTTRS = Text.DEFAULTATTRS

    def __init__(self, *attrs, **kwargs):
        super().__init__(*attrs, **kwargs)

    def setup(self, parent):
        super().setup(parent)
        newtime = time.localtime()
        self.time = (newtime[2], newtime[1])
        self.update(message=time.strftime("%A, %d %B",newtime))

    def draw(self, surface):
        newtime = time.localtime()
        if self.time[0] != newtime[2] or self.time[1] != newtime[1]:
            self.time = (newtime[2], newtime[1])
            self.update(message=time.strftime("%A, %d %B",newtime))
        super().draw(surface)
