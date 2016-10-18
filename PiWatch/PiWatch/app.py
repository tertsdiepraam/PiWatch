"""Defines the classes for the construction of PiWatch-apps."""
import os

from .event import EventHandler
from .event import EventListener


class Activity(EventListener):
    def __init__(self, name):
        self.name = name
        self.objects = []  # later objects are drawn OVER earlier objects
        EventListener.__init__(self)

    def add(self, *args):
        for object in args:
            self.objects.append(object)

    def setup(self, parent):
        for object in self.objects:
            object.setup(parent)

    def draw(self, surface):
        for object in self.objects:
            object.draw(surface)


class App(EventHandler):
    def __init__(self, name='app', bg_color=(0, 0, 0), icon=None):
        self.name = name
        self.icon = icon
        self.bg_color = bg_color
        self.activities = {}
        self.mainactivity = 'main'
        self.current_activity = None
        self.folder = 'apps' + os.sep + name + os.sep
        EventHandler.__init__(self)

    def start(self, parent):
        self.current_activity = self.activities[self.mainactivity]
        self.current_activity.setup(parent)

    def add(self, *args):
        for activity in args:
            self.activities[activity.name] = activity

    def draw(self, surface):
        self.current_activity.draw(surface)

    def get_event_listeners(self):
        d1 = self.event_listeners.copy()
        d1_keys = d1.keys()
        d2 = self.current_activity.get_event_listeners().items()
        for key, value in d2:
            if key in d1_keys:
                d1[key] += value
            else:
                d1[key] = value
        return d1


class Service(EventHandler):
    def __init__(self, name='Anonymous Service'):
        self.name = name
        EventHandler.__init__(self)

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def pause(self):
        raise NotImplementedError()


