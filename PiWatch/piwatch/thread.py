import threading


def threaded(func):
    """A decorator which converts a function to a ThreadedFunction."""
    func_thread = ThreadedFunction(target=func)
    return func_thread


class ThreadedFunction:
    """A thread which calls a function every time it is called."""
    def __init__(self, target=None, *args, **kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.thread = threading.Thread(target=self.target, args=self.args, kwargs=self.kwargs)
        self.thread.daemon = True
        self.thread.start()
