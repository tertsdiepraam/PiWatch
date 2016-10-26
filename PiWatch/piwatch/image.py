"""This file provides the text classes for PiWatch-apps."""
import pygame

from .drawable import *


class ImageAttrs(AttrSet):
    def set_defaults(self):
        super().set_defaults()
        self.attrs.update({
            'filename': None,
            'size_x': None,
            'size_y': None})


class Image(PiDrawable):
    DEFAULTATTRS = ImageAttrs()

    def setup(self, parent):
        self.file = pygame.image.load(self.filename)
        self.image = self.file
        self.rect = self.image.get_rect()
        self.render_image()
        super().setup(parent)

    def render_image(self):
        if not (self.size_x or self.size_y):
            size_x = self.rect.width
            size_y = self.rect.height
        elif self.size_x and not self.size_y:
            size_x = self.size_x
            size_y = int(self.size_x * self.rect.height / self.rect.width)
        elif self.size_y and not self.size_x:
            size_x = int(self.size_y * self.rect.width / self.rect.height)
            size_y = self.size_y
        else:
            size_x = self.size_x
            size_y = self.size_y
        self.image = pygame.transform.scale(self.file, (size_x, size_y))

    def update(self, **kwargs):
        if 'filename' in kwargs.keys():
            self.filename = kwargs['filename']
            self.file = pygame.image.load(self.filename)
            del kwargs['filename']
        super().update(**kwargs)
