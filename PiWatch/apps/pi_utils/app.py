"""Defines the classes for the construction of PiWatch-apps."""


class Activity:
    def __init__(self, name):
        self.name = name
        self.objects = []  # later objects are drawn OVER earlier objects
        self.event_listeners = {}

    def add(self, *args):
        for object in args:
            self.objects.append(object)

    def setup(self, parent):
        for object in self.objects:
            object.setup(parent)

    def draw(self, surface):
        for object in self.objects:
            object.draw(surface)

    def event_listener(self, event_type):
        def add_listener(func):
            if not event_type in self.event_listeners.keys():
                self.event_listeners[event_type] = []
            self.event_listeners[event_type].append(func)
        return add_listener


class App:
    def __init__(self, name='app', bg_color=(0, 0, 0), icon=None):
        self.name = name
        self.icon = icon
        self.bg_color = bg_color
        self.activities = {}
        self.mainactivity = 'main'
        self.currentactivity = None
        self.app_event_listeners = {}

    def start(self, parent):
        self.currentactivity = self.activities[self.mainactivity]
        self.currentactivity.setup(parent)

    def add(self, *args):
        for activity in args:
            self.activities[activity.name] = activity

    def draw(self, surface):
        self.currentactivity.draw(surface)

    def event_listener(self, event_type):
        def add_listener(func):
            if not event_type in self.app_event_listeners.keys():
                self.app_event_listeners[event_type] = []
            self.app_event_listeners[event_type].append(func)
        return add_listener

    @property
    def event_listeners(self):
        d1 = self.app_event_listeners.copy()
        d1_keys = d1.keys()
        d2 = self.currentactivity.event_listeners.items()
        for key, value in d2:
            if key in d1_keys:
                d1[key] += value
            else:
                d1[key] = value
        return dict(d1)
