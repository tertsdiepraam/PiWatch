"""Defines the classes for the construction of PiWatch-apps."""
from .base import *


class Activity:
    def __init__(self, name):
        self.name = name
        self.objects = []  # later objects are drawn OVER earlier objects

    def add(self, *args):
        for object in args:
            self.objects.append(object)

    def setup(self, parent):
        for object in self.objects:
            object.setup(parent)

    def respond(self, pos):
        response = []
        for object in self.objects:
            try:
                response += object.respond(pos)
            except AttributeError:
                pass
        for function in response:
            call(function)

    def draw(self, surface):
        for object in self.objects:
            object.draw(surface)


class App:
    def __init__(self, name='app', bg_color=(0, 0, 0), icon=None):
        self.name = name
        self.icon = icon
        self.bg_color = bg_color
        self.activities = {}
        self.mainactivity = 'main'
        self.currentactivity = None


def start(self, parent):
    self.currentactivity = self.activities[self.mainactivity]
    self.currentactivity.setup(parent)


def add(self, *args):
    for activity in args:
        self.activities[activity.name] = activity


def draw(self, surface):
    self.currentactivity.draw(surface)
