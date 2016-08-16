from .drawable import *


class GroupAttrs(AttrSet):
    def set_defaults():
        AttrSet.set_defaults(self)
        self.childs = []


class Group(PiDrawable):
    def __init__(self, attr):
        PiDrawable.__init__(self, attr)
        if attr.childs:
            self.childs = attr.childs
        else:
            self.childs = []

    def add(self, *args):
        for object in args:
            self.objects.append(object)

    def update(self):
        for object in self.objects:
            object.set_pos(addpos_x=self.position[0], addpos_y=self.position[1])
        self.rect = self.objects[0].rect.unionall([object.rect for object in self.objects[1:]])

    def draw(self, surface):
        super().draw(surface)
