import datetime


def get_time():
    return datetime.datetime.now().time()


def time_to_str(time):
    return time.strftime('%H:%M:%S')


def return_event(target):
    def outer(func):
        def inner(event):
            target.eventqueue.add(func(event))

        return inner

    return outer
