from .drawable import *
import pygame

class Group(PiDrawable):
    DEFAULTATTRS = dict(
        PiDrawable.DEFAULTATTRS,
        children=[]
    )

    def add(self, *args):
        for child in args:
            self.children.append(child)
            if hasattr(self, 'parent'):
                child.setup(self.parent)
        if hasattr(self, 'parent'):
            self.set_position()

    def clear(self):
        self.children = []

    def setup(self, parent):
        self.parent = parent
        for child in self.children:
            child.setup(parent)
        self.set_position()

    def render_image(self):
        for child in self.children:
            child.render_image()

    def set_position(self):
        for child in self.children:
            child.set_position()
        self.rect = self.children[0].rect.unionall([child.rect for child in self.children[1:]])

    def draw(self, surface):
        if self.bg_color:
            surface.fill(self.bg_color, self.rect.inflate(self.padding[0], self.padding[1]))
        for child in self.children:
            child.draw(surface)


class List(Group):
    DEFAULTATTRS = dict(
        Group.DEFAULTATTRS,
        direction='down',
        padding=0,
        alignment='midtop'
    )

    def get_standalone_rect(self):
        child_rects = [child.get_standalone_rect() for child in self.children]
        if self.direction in ['left', 'right']:
            return pygame.Rect(0, 0,
                               sum(rect.width for rect in child_rects)
                               + (len(self.children)-1) * self.padding[0],
                               max(rect.height for rect in child_rects)
                               )
        elif self.direction in ['up', 'down']:
            return pygame.Rect(0, 0,
                               max(rect.width for rect in child_rects),
                               sum(rect.height for rect in child_rects)
                               + (len(self.children)-1) * self.padding[1]
                               )

    def set_position(self):
        self.rect = self.get_standalone_rect()
        self.parent_rect = self.parent.get_rect()
        if type(self.position) is str:
            setattr(self.rect, self.position, getattr(self.parent_rect, self.position))
        elif type(self.position) is tuple:
            setattr(self.rect, self.position[0], getattr(self.parent_rect, self.position[0]))
            self.rect.move_ip(self.position[1], self.position[2])
        else:
            raise AttributeError
        self.set_pos_from_rect_children()

    def set_pos_from_rect_children(self):
        if self.direction == 'right':
            offset = self.rect.left
            for child in self.children:
                child.set_pos_from_rect(
                    pygame.Rect(offset, self.rect.top, child.get_standalone_rect().width, self.rect.height), self.alignment)
                offset += child.get_standalone_rect().width + self.padding[0]
        elif self.direction == 'down':
            offset = self.rect.top
            for child in self.children:
                child.set_pos_from_rect(
                    pygame.Rect(self.rect.left, offset, self.rect.width, child.get_standalone_rect().height), self.alignment)
                offset += child.get_standalone_rect().height + self.padding[1]

    def set_pos_from_rect(self, rect, alignment):
        self.rect = self.get_standalone_rect()
        setattr(self.rect, alignment, getattr(rect, alignment))
        self.set_pos_from_rect_children()


class Grid(List):
    def add(self, *args):
        for row in args:
            self.children.append(row)
            for item in row:
                if hasattr(self, 'parent'):
                    item.setup(self.parent)
        if hasattr(self, 'parent'):
            self.set_position()

    def setup(self, parent):
        self.parent = parent
        for row in self.children:
            for item in row:
                item.setup(parent)
        print(self.children)
        self.set_position()

    def draw(self, surface):
        if self.bg_color:
            surface.fill(self.bg_color, self.rect.inflate(self.padding[0], self.padding[1]))
        for row in self.children:
            for item in row:
                item.draw(surface)

    def render_image(self):
        for row in self.children:
            for item in row:
                item.render_image()

    def get_standalone_rect(self):
        if self.direction == 'down':
            width = 0
            height = 0
            for row in self.children:
                rects = [item.get_standalone_rect() for item in row]
                width += sum(rect.width for rect in rects) + self.padding[0] * len(rects[:-1])
                height += max(rect.height for rect in rects)
            height += self.padding[0] * len(self.children[:-1])
        return pygame.Rect(0, 0, width, height)

    def set_pos_from_rect_children(self):
        if not self.children:
            return
        child_rects = [item.get_standalone_rect() for row in self.children for item in row]
        item_height = max(rect.height for rect in child_rects)
        item_width = max(rect.width for rect in child_rects)
        init_offset_x = self.rect.left
        init_offset_y = self.rect.top
        item_offset_x = item_width + self.padding[0]
        item_offset_y = item_height + self.padding[1]
        if self.direction == 'down':
            for y_index, row in enumerate(self.children):
                for x_index, item in enumerate(row):
                    _x = init_offset_x + x_index * item_offset_x
                    _y = init_offset_y + y_index * item_offset_y
                    item.set_pos_from_rect(
                        pygame.Rect(_x, _y, item_width, item_height),
                        self.alignment
                    )
