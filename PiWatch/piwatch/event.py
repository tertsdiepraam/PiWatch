"""Event classes"""
import datetime
import sys

import pygame

if sys.platform == 'linux':
    # Raspberry Pi GPIO setup
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(12, GPIO.RISING)
    GPIO.add_event_detect(16, GPIO.RISING)
    GPIO.add_event_detect(18, GPIO.RISING)

class Event:
    def __init__(self, event_type, source=None, target=None, data=None, key=None, pos=None):
        self.timestamp = datetime.datetime.now().time()
        self.type = event_type
        self.source = source
        self.target = target
        self.data = data
        self.key = key
        self.pos = pos


class Eventqueue:
    def __init__(self):
        self.events = []
        self.time = datetime.datetime.now().time()

    def add(self, *args, **kwargs):
        if len(args) == 1 and type(args[0]) is str:
            if 'data' in kwargs.keys():
                self.events.append(Event(args[0], data=kwargs['data'], source=self))
            else:
                self.events.append(Event(args[0]), source=self)
        for event in args:
            if not hasattr(event, 'source'):
                event.source = self
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
                self.add(Event('mouse up', pos=event.pos))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.add(Event('mouse down', pos=event.pos))
                print("mouse up at {}".format(event.pos))

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
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
            if event.target:
                for func in event.target.get_event_listeners()[event.type]:
                    func(event)
            else:
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
            return func
        return add_listener

    def get_event_listeners(self):
        return self.event_listeners


class EventHandler(EventListener):
    def __init__(self):
        self.eventqueue = Eventqueue()
        self.global_eventqueue = Eventqueue()
        EventListener.__init__(self)

