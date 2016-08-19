import threading


def threaded(func):
    func_thread = ThreadedFunction(target=func)
    return func_thread


class ThreadedFunction():
    def __init__(self, target=None, *args, **kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.thread = threading.Thread(target=self.target, args=self.args, kwargs=self.kwargs)
        self.thread.start()