"""Event classes"""
import datetime
import sys

import pygame


class Event:
    def __init__(self, event_type, key=None, pos=None, msg=None):
        self.timestamp = datetime.datetime.now().time()
        self.type = event_type.lower()
        self.key = key
        self.pos = pos
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
        new_time = datetime.datetime.now().time()
        if self.time != new_time:
            self.time = new_time
            self.add(Event('time'))

        # pygame specific event handling
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                self.add(Event('mouse_up', pos=event.pos))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.add(Event('mouse_down', pos=event.pos))

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

            elif event.type == pygame.QUIT:
                sys.exit()

    def import_events(self, *other_queues):
        for queue in other_queues:
            self.events += queue.events

    def broadcast(self, *targets, clear=True):
        for event in self.events:
            for target in targets:
                if event.type in target.event_listeners.keys():
                    for func in target.event_listeners[event.type]:
                        func(event)
        if clear:
            self.clear()
