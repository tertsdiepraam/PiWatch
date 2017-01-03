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
        padding=None,
        fixed_size=None,
        color=(0, 0, 0, 255),
        visible=True
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
        if type(self.fixed_size) is int:
            self.fixed_size = (self.fixed_size, self.fixed_size)
        if hasattr(self, 'color'):
            if len(self.color) == 3:
                self.color += (255,)
        if hasattr(self, 'bg_color'):
            if self.bg_color and len(self.bg_color) == 3:
                self.bg_color += (255,)

    def set_attrs(self, attrdict):
        for attr, value in attrdict.items():
            setattr(self, attr, value)

    def setup(self, parent):
        self.parent = parent
        self.full_render()

    def update(self, **kwargs):
        set_pos, set_fg, set_bg, full_render = False, False, False, False
        if kwargs:
            self.set_attrs(kwargs)
        else:
            self.full_render()
            return
        if not {'message', 'font', 'size_x', 'size_y', 'filename', 'size'}.isdisjoint(set(kwargs.keys())):
            full_render = True
        else:
            if 'position' in kwargs.keys():
                set_pos = True
            if 'color' in kwargs.keys():
                if len(self.color) == 3:
                    self.color += (255,)
                set_fg = True
        if not {'bg_color', 'padding', 'fixed_size'}.isdisjoint(set(kwargs.keys())):
            if hasattr(self, 'bg_color') and self.bg_color:
                if len(self.bg_color) == 3:
                    self.bg_color += (255,)
            if type(self.padding) is int:
                self.padding = (self.padding, self.padding)
            if type(self.fixed_size) is int:
                self.fixed_size = (self.fixed_size, self.fixed_size)
            set_bg = True

        if full_render:
            self.full_render()
            return
        if set_pos:
            self.set_position()
        if set_fg:
            self.create_fg_surf()
        if set_bg:
            self.create_bg_surf()

    def full_render(self):
        self.render_image()
        self.set_position()
        self.create_surfaces()

    def set_position(self):
        self.fg_rect = self.image.get_rect()
        self.parent_rect = self.parent.get_rect()
        if type(self.position) is str:
            setattr(self.fg_rect, self.position, getattr(self.parent_rect, self.position))
        elif type(self.position) is tuple:
            setattr(self.fg_rect, self.position[0], getattr(self.parent_rect, self.position[0]))
            self.fg_rect.move_ip(self.position[1], self.position[2])
        else:
            raise AttributeError
        if self.padding and self.fixed_size:
            raise AttributeError("Drawable " + str(type(self)) + " can't have both padding and fixed_size attributes")
        if self.padding:
            self.bg_rect = self.fg_rect.inflate(self.padding[0], self.padding[1])
        elif self.fixed_size:
            self.bg_rect = pygame.Rect(0, 0, self.fixed_size[0], self.fixed_size[1])
            self.bg_rect.center = self.fg_rect.center
        else:
            self.bg_rect = self.fg_rect

    def get_standalone_rect(self):
        rect = self.image.get_rect()
        if self.padding:
            rect = pygame.Rect(0, 0, rect.width+self.padding[0], rect.height+self.padding[1])
        elif self.fixed_size:
            rect = pygame.Rect(0, 0, self.fixed_size[0], self.fixed_size[1])
        return pygame.Rect(0, 0, rect.width, rect.height)

    def set_pos_from_rect(self, rect, alignment):
        self.bg_rect = self.get_standalone_rect()
        if self.padding and self.fixed_size:
            raise AttributeError("Drawable " + str(type(self)) + " can't have both padding and fixed_size attributes")

        if self.padding:
            setattr(self.bg_rect, alignment, getattr(rect.inflate(-self.padding[0], -self.padding[1]), alignment))
            self.fg_rect = self.bg_rect.inflate(-self.padding[0], -self.padding[1])

        elif self.fixed_size:
            setattr(self.bg_rect, alignment, getattr(rect, alignment))
            self.fg_rect = self.image.get_rect()
            setattr(self.fg_rect, self.position[0], getattr(self.bg_rect, self.position[0]))

        else:
            setattr(self.bg_rect, alignment, getattr(rect, alignment))
            self.fg_rect = self.bg_rect

    def create_bg_surf(self):
        """Create the surface that represents the background of the object."""
        if self.bg_color:
            self.bg_surf = pygame.Surface((self.bg_rect.width, self.bg_rect.height))
            self.bg_surf.fill(self.bg_color)
            if len(self.bg_color) == 4 and self.bg_color[3] != 255:
                self.bg_surf.set_alpha(self.bg_color[3])

    def create_fg_surf(self):
        """Create the surface that represents the foreground of the object."""
        if self.image:
            if len(self.color) == 4 and self.color[3] != 255:
                self.fg_surf = self.image.copy()
                pixelarray = pygame.PixelArray(self.fg_surf)
                for x in range(self.image.get_width()):
                    for y in range(self.image.get_height()):
                        pixel = self.image.unmap_rgb(pixelarray[x, y])
                        if not pixel[3] == 0:
                            pixelarray[x, y] = self.image.map_rgb(pixel[:3] + (int(pixel[3] * self.color[3] / 255),))
            else:
                self.fg_surf = self.image

    def create_surfaces(self):
        self.create_bg_surf()
        self.create_fg_surf()

    def draw(self, surface):
        if hasattr(self, 'bg_surf') and self.bg_surf:
            surface.blit(self.bg_surf, self.bg_rect)
        if hasattr(self, 'fg_surf') and self.fg_surf:
            surface.blit(self.fg_surf, self.fg_rect)

    def check_collision(self, point):
        return self.bg_rect.collidepoint(point)

    def render_image(self):
        raise NotImplementedError("Render Image is specific for subclasses and needs to be defined.")

    @property
    def attributes(self):
        return self.DEFAULTATTRS

    @classproperty
    def attributes(self):
        return self.DEFAULTATTRS
