# for calling functions from clickables etc.
def call(func):
    try:
        func()
    except TypeError:
        function, *args = func
        function(*args)
