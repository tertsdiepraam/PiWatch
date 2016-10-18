import time
from piwatch import *


def define_app():

    app = App(
        name="notification"
    )
    title = Text(
        color=(0, 0, 0),
        size=20,
        position=('midtop', 0, 0)
    )

    text = Text(
        color=(0, 0, 0),
        size=17,
        position=('midtop', 0, 25)
    )
    notification = Group(
        bg_color=(200, 200, 200),
        padding=(40, 5)
    )
    notification.add(title, text)

    main = Activity(
        name='main'
    )

    empty = Activity(
        name='empty'
    )
    app.thread_count = 0

    @app.event_listener('notification')
    @threaded
    def display_notification(event):
        app.thread_count += 1
        title.update(message=event.data[1])
        text.update(message=event.data[2])
        app.current_activity = main
        time.sleep(3)
        if app.thread_count == 1:
            app.current_activity = empty
        app.thread_count -= 1

    main.add(notification)
    app.add(main, empty)

    return app
