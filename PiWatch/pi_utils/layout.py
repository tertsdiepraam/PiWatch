from .drawable import *

class GroupAttrs(AttrSet):
    def set_defaults(self):
        super().set_defaults()
        self.attrs.update({
            'children': []
        })


class Group(PiDrawable):
    DEFAULTATTRS = GroupAttrs()

    def add(self, *args):
        for child in args:
            self.children.append(child)
            if hasattr(self, 'parent'):
                child.setup(self.parent)

    def clear(self):
        self.children = []

    def setup(self, parent):
        self.parent = parent
        for child in self.children:
            child.setup(parent)
        self.set_position()

    def set_position(self):
        for child in self.chilren:
            child.set_position()
        self.rect = self.children[0].rect.unionall([child.rect for child in self.children[1:]])

    def draw(self, surface):
        if self.bg_color:
            surface.fill(self.bg_color, self.rect)
        for child in self.children:
            child.draw(surface)


class List(Group):
    def set_position(self):
        offset = 0
        if self.children:
            for child in self.children:
                if type(child) is str:
                    child = str_to_text(child)
                child.update(position=(self.position[0], self.position[1], self.position[2]+offset))
            self.rect = self.children[0].rect.unionall([child.rect for child in self.children[1:]])
        else:
            self.rect = None