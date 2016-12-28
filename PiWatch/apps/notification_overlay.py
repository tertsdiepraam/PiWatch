import time
from piwatch import *


def define_overlay():

    app = App(
        name="notification"
    )
    title = Text(
        color=(255, 255, 255),
        size=25,
    )

    text = Text(
        color=(255, 255, 255),
        size=20,
    )
    notification = List(
        children=[title, text],
        bg_color=(50, 50, 50, 230),
        fixed_size=(250, 55),
        direction='down',
        alignment='center',
        spacing=10,
        position=('midtop', 0, 20)
    )

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
        app.set_activity('main')
        time.sleep(3)
        if app.thread_count == 1:
            app.set_activity('empty')
        app.thread_count -= 1

    main.add(notification)
    app.add(main, empty)

    return app
