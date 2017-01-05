from .drawable import *
import pygame
import itertools


class Group(Drawable):
    DEFAULTATTRS = dict(
        Drawable.DEFAULTATTRS,
        children=[]
    )

    def add(self, *args):
        for child in args:
            self.children.append(child)
            if hasattr(self, 'parent'):
                child.setup(self.parent)
        if hasattr(self, 'parent'):
            self.set_position()
            self.create_bg_surf()

    def clear(self):
        self.children = []

    def setup(self, parent):
        self.parent = parent
        for child in self.children:
            child.setup(parent)
        self.set_position()
        self.create_bg_surf()

    def render_image(self):
        for child in self.children:
            child.render_image()

    def set_position(self):
        for child in self.children:
            child.set_position()
        self.bg_rect = self.children[0].bg_rect.unionall([child.bg_rect for child in self.children[1:]])
        print(self.bg_rect)

    def draw(self, surface):
        if hasattr(self, 'bg_surf') and self.bg_surf:
            surface.blit(self.bg_surf, self.bg_rect)
        for child in self.children:
            child.draw(surface)


class List(Group):
    DEFAULTATTRS = dict(
        Drawable.DEFAULTATTRS,
        direction='down',
        alignment='midtop',
        children=[],
        spacing=0
    )

    def update(self, **kwargs):
        if kwargs:
            self.set_attrs(kwargs)
        if hasattr(self, 'bg_color') and self.bg_color:
            if len(self.bg_color) == 3:
                self.color += 255
                self.create_bg_surf()
        self.render_image()
        self.set_position()
        self.create_bg_surf()

    def get_standalone_rect(self):
        if not self.children:
            return pygame.Rect(0, 0, 0, 0)
        if self.fixed_size:
            return pygame.Rect(0, 0, self.fixed_size[0], self.fixed_size[1])
        child_rects = [child.get_standalone_rect() for child in self.children]
        if self.direction in ['left', 'right']:
            rect = pygame.Rect(0, 0,
                               sum(rect.width for rect in child_rects)
                               + (len(self.children)-1) * self.spacing,
                               max(rect.height for rect in child_rects)
                               )
        elif self.direction in ['up', 'down']:
            rect = pygame.Rect(0, 0,
                               max(rect.width for rect in child_rects),
                               sum(rect.height for rect in child_rects)
                               + (len(self.children)-1) * self.spacing
                               )
        if self.padding:
            return rect.inflate(self.padding[0], self.padding[1])
        return rect

    def set_position(self):
        self.fg_rect = self.get_standalone_rect()
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
        self.create_bg_surf()
        self.set_pos_from_rect_children()

    def set_pos_from_rect_children(self):
        if self.direction == 'right':
            offset = self.fg_rect.left
            for child in self.children:
                child_rect = child.get_standalone_rect()
                child.set_pos_from_rect(
                    pygame.Rect(offset, self.fg_rect.top, child_rect.width, self.fg_rect.height), self.alignment)
                offset += child_rect.width + self.spacing
        elif self.direction == 'down':
            offset = self.fg_rect.top
            for child in self.children:
                child_rect = child.get_standalone_rect()
                child.set_pos_from_rect(
                    pygame.Rect(self.fg_rect.left, offset, self.fg_rect.width, child_rect.height), self.alignment)
                offset += child_rect.height + self.spacing

    def set_pos_from_rect(self, rect, alignment):
        self.fg_rect = self.get_standalone_rect()
        setattr(self.fg_rect, alignment, getattr(rect, alignment))
        self.set_pos_from_rect_children()

        if self.padding and self.fixed_size:
            raise AttributeError("Drawable " + str(type(self)) + " can't have both padding and fixed_size attributes")
        if self.padding:
            self.bg_rect = self.fg_rect.inflate(self.padding[0], self.padding[1])
        elif self.fixed_size:
            self.bg_rect = pygame.Rect(0, 0, self.fixed_size[0], self.fixed_size[1])
            self.bg_rect.center = self.fg_rect.center
        else:
            self.bg_rect = self.fg_rect


class Grid(List):
    def add(self, *args):
        for row in args:
            self.children.append(row)
            for item in row:
                if hasattr(self, 'parent'):
                    item.setup(self.parent)
        if hasattr(self, 'parent'):
            self.set_position()
            self.create_bg_surf()

    def setup(self, parent):
        self.parent = parent
        for row in self.children:
            for item in row:
                item.setup(parent)
        self.set_position()
        self.create_bg_surf()

    def draw(self, surface):
        if self.bg_color:
            surface.blit(self.bg_surf, self.bg_rect)
        for row in self.children:
            for item in row:
                item.draw(surface)

    def render_image(self):
        for row in self.children:
            for item in row:
                item.render_image()

    def get_standalone_rect(self):
        if not self.children:
            return pygame.Rect(0, 0, 0, 0)
        if self.direction == 'down':
            row_widths = []
            height = 0
            for row in self.children:
                rects = [item.get_standalone_rect() for item in row]
                row_widths.append(max(rect.width for rect in rects) * len(rects) + self.spacing * len(rects[:-1]))
                height += max(rect.height for rect in rects)
            height += self.spacing * len(self.children[:-1])
            width = max(row_widths)
        return pygame.Rect(0, 0, width, height)

    def set_pos_from_rect_children(self):
        if self.children:
            child_rects = [item.get_standalone_rect() for row in self.children for item in row]
            item_height = max(rect.height for rect in child_rects)
            item_width = max(rect.width for rect in child_rects)
            init_offset_x = self.fg_rect.left
            init_offset_y = self.fg_rect.top
            item_offset_x = item_width + self.spacing
            item_offset_y = item_height + self.spacing
            if self.direction == 'down':
                for y_index, row in enumerate(self.children):
                    for x_index, item in enumerate(row):
                        _x = init_offset_x + x_index * item_offset_x
                        _y = init_offset_y + y_index * item_offset_y
                        item.set_pos_from_rect(
                            pygame.Rect(_x, _y, item_width, item_height),
                            self.alignment
                        )

    @property
    def flat_children(self):
        return itertools.chain.from_iterable(self.children)
