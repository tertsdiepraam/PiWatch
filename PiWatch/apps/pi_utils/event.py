"""Event classes"""


class Event:
    def __init__(self, timestamp):
        self.timestamp


class MouseEvent(Event):
    """Baseclass for MouseDownEvent and MouseUpEvent"""
    def __init__(self, timestamp, position):
        super().__init__(timestamp)
        self.position = position


class MouseDownEvent(MouseEvent):
    """Event that is triggered if left mouse button is pressed."""
    pass


class MouseUpEvent(MouseEvent):
    """Event that is triggered if left mouse button is released."""
    pass


class KeyEvent(Event):
    """Baseclass for KeyDownEvent and KeyUpEvent."""
    def __init__(self, timestamp, key):
        super().__init__(timestamp)
        self.key = key


class KeyDownEvent(KeyEvent):
    """Event that is triggered if a key is pressed."""
    pass


class KeyUpEvent(KeyEvent):
    """Event that gets triggered if a key is released."""
    pass


class TimeEvent(Event):
    """Event that is triggered if there is a change in time."""
    pass

class SignalEvent(Event):
    def __init__(self, timestamp, signal):
        super().__init__(timestamp)
        self.signal = signal

class Eventqueue:
    def __init__(self):
        self.events = []

    def add(self, *args):
        for event in args:
            self.events.append(event)

    def clear(self):
        self.events = []

    def broadcast(self, *targets):
        for event in self.events:
            pass