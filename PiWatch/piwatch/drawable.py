"""This file defines the abstract classes which provide basic component functionality."""
from piwatch.base_functions import classproperty
import pygame

# All drawable classes must inherit from this class
class PiDrawable:
    """Base class for drawables, takes an AttrSet object and additional kwargs as arguments"""
    DEFAULTATTRS = dict(
        bg_color=None,
        position=('center', 0, 0),
        image=None,
        function=None,
        padding=(0, 0),
        fixed_size=None
    )

    def __init__(self, *attrs, **kwargs):
        if attrs:
            for attrset in attrs:
                self.set_attrs(attrset)
        else:
            self.set_attrs(self.DEFAULTATTRS)
        self.set_attrs(kwargs)
        if type(self.padding) is int:
            self.padding = (self.padding, self.padding)

    def set_attrs(self, attrdict):
        for attr, value in attrdict.items():
            setattr(self, attr, value)

    def setup(self, parent):
        self.parent = parent
        self.set_position()

    def update(self, **kwargs):
        if kwargs:
            self.set_attrs(kwargs)
        self.render_image()
        if 'position' in kwargs.keys():
            self.set_position()

    def set_position(self):
        self.rect = self.image.get_rect()
        self.parent_rect = self.parent.get_rect()
        if type(self.position) is str:
            exec('self.rect.' + self.position + ' = self.parent_rect.' + self.position)
        elif type(self.position) is tuple:
            exec('self.rect.' + self.position[0] + ' = self.parent_rect.' + self.position[0])
            self.rect.move_ip(self.position[1], self.position[2])
        else:
            raise AttributeError
        if self.padding and self.fixed_size:
            raise AttributeError('Drawable')

    def get_standalone_rect(self):
        rect = self.image.get_rect()
        return pygame.Rect(0, 0, rect.width, rect.height)

    def set_pos_from_rect(self, rect, alignment):
        self.rect = self.get_standalone_rect()
        setattr(self.rect, alignment, getattr(rect, alignment))

    def draw(self, surface):
        if self.bg_color:
            surface.fill(self.bg_color, self.rect.inflate(self.padding[0], self.padding[1]))
        surface.blit(self.image, self.rect)

    def check_collision(self, point):
        return self.rect.collidepoint(point)

    @property
    def attributes(self):
        return self.DEFAULTATTRS

    @classproperty
    def attributes(self):
        return self.DEFAULTATTRS
