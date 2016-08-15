""""Request classes"""


class Request:
    def __init__(self, app, requested_action):
        self.app = app
        self.action = requested_action


class Requestqueue:
    def __init__(self):
        self.requests = []
