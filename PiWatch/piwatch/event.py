"""Event classes"""
import datetime
import sys

import pygame

if sys.platform == 'linux':
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(12, GPIO.RISING)
    GPIO.add_event_detect(16, GPIO.RISING)
    GPIO.add_event_detect(18, GPIO.RISING)

class Event:
    def __init__(self, event_type, key=None, pos=None, data=None):
        self.timestamp = datetime.datetime.now().time()
        self.type = event_type
        self.key = key
        self.pos = pos
        self.data = data


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

        # RPi GPIO input event handling
        if sys.platform == 'linux':
            if GPIO.event_detected(12):
                pass
            if GPIO.event_detected(16):
                self.add(Event('main start app', data='Home'))
            if GPIO.event_detected(18):
                self.add(Event('main start app', data='appdrawer'))

        # pygame specific event handling
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                self.add(Event('mouse_up', pos=event.pos))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.add(Event('mouse_down', pos=event.pos))

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_q:
                    pass
                elif event.key == pygame.K_a:
                    self.add(Event('main start app', data='Home'))
                elif event.key == pygame.K_z:
                    self.add(Event('main start app', data='appdrawer'))

            elif event.type == pygame.QUIT:
                sys.exit()

    def import_events(self, *event_handlers, clear=True):
        for handler in event_handlers:
            if type(handler) is Eventqueue:
                queue = handler
            else:
                queue = handler.global_eventqueue
            self.events += queue.events
            if clear:
                queue.clear()

    def broadcast(self, *targets, clear=True):
        for event in self.events:
            if not event: continue
            for target in targets:
                if event.type in target.get_event_listeners().keys():
                    for func in target.get_event_listeners()[event.type]:
                        func(event)
        if clear:
            self.clear()


class EventListener:
    def __init__(self):
        self.event_listeners = {}

    def event_listener(self, event_type):
        def add_listener(func):
            if event_type not in self.event_listeners.keys():
                self.event_listeners[event_type] = []
            self.event_listeners[event_type].append(func)
        return add_listener

    def get_event_listeners(self):
        return self.event_listeners


class EventHandler(EventListener):
    def __init__(self):
        self.eventqueue = Eventqueue()
        self.global_eventqueue = Eventqueue()
        EventListener.__init__(self)

