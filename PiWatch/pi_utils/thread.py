import threading


def thread(func):
    func_thread = ThreadFunction(target=func)
    return func_thread


class ThreadFunction():
    def __init__(self, target=None, *args, **kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        print('starting thread_func')
        self.args = args
        self.kwargs = kwargs
        self.thread = threading.Thread(target=self.target, args=self.args, kwargs=self.kwargs)
        self.thread.start()