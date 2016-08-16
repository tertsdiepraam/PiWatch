"""This file defines the abstract classes which provide basic component functionality."""

# AttributeSet is the object that gets passed to a drawable
class AttrSet:
    def __init__(self, **kwargs):
        self.attrs = {}
        self.setDefaults()
        self.setAttrs(kwargs)

    def setAttrs(self, attrdict):
        for attr, value in attrdict.items():
            setattr(self, attr, value)

    def setDefaults(self):
        self.attrs.update(
            {'bg_color': None,
             'position': ('center', 0, 0),
             'image': None,
             'function': None,
             'padding': (0, 0)})


# All drawable classes must inherit from this class
class PiDrawable:
    '''Base class for drawables, takes an AttrSet object and additional kwargs as arguments'''
    DEFAULTATTRS = AttrSet()

    def __init__(self, *attrs, **kwargs):
        if attrs:
            for attrset in attrs:
                self.set_attrs(attrset.attrs)
        else:
            self.set_attrs(self.DEFAULTATTRS.attrs)
        self.set_attrs(kwargs)
        if type(self.padding) is int:
            self.padding = (self.padding, self.padding)

    def set_attrs(self, attrdict):
        for attr, value in attrdict.items():
            setattr(self, attr, value)

    def set_pos(self, addpos_x=None, addpos_y=None):
        if not addpos_x:
            addpos_x = 0
        if not addpos_y:
            addpos_y = 0
        self.rect = self.image.get_rect()
        self.parent_rect = self.parent.get_rect()
        if type(self.position) is str:
            exec('self.rect.' + self.position + ' = self.parent_rect.' + self.position)
        elif type(self.position) is tuple:
            exec('self.rect.' + self.position[0] + ' = self.parent_rect.' + self.position[0])
            self.rect.move_ip(self.position[1] + addpos_x, self.position[2] + addpos_y)
        else:
            raise AttributeError

    def draw(self, surface):
        if self.bg_color:
            surface.fill(self.bg_color, self.rect)
        surface.blit(self.image, self.rect)
