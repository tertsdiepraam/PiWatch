"""Event classes"""
import datetime

import pygame

from .functions import call


class Event:
    def __init__(self, timestamp, event_type, key=None, pos=None, msg=None):
        self.timestamp = timestamp
        self.type = event_type.lower()
        self.key = key
        self.position = pos
        self.msg = msg

class Eventqueue:
    def __init__(self):
        self.events = []
        self.time = datetime.datetime.now().time()

    def add(self, *args):
        for event in args:
            self.events.append(event)

    def clear(self):
        self.events = []

    def handle_events(self):
        newtime = datetime.datetime.now().time()
        if self.time != newtime:
            self.time = newtime
            self.add(Event(self.time, 'time'))

        # pygame specific event handling
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                self.add(Event(self.time, 'mouse_up', pos=event.pos))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.add(Event(self.time, 'mouse_down', pos=event.pos))

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

            elif event.type == pygame.QUIT:
                sys.exit()

    def broadcast(self, *targets, clear=True):
        for event in self.events:
            for target in targets:
                if event.type in target.event_listeners.keys():
                    for func in target.event_listeners[event.type]:
                        call(func)
        if clear:
            self.clear()
