import time
from piwatch import *

def define_app():

    app = App(
        name="notification"
    )
    title = Text(
        message="Message from Maria",
        color=(0, 0, 0),
        size=20,
        position=('midtop', 0, 0)
    )

    text = Text(
        message="Trololololo",
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

    @app.event_listener('start')
    def on_start(event):
        app.id = random.randInt(0, 1000)

    @app.event_listener('notification')
    @threaded
    def display_notification(event):
        title.update(message=event.data[1])
        text.update(message=event.data[2])
        time.sleep(1)
        print("Closing overlay")
        app.global_eventqueue.add(Event('main close overlay', data='notification'))

    main.add(notification)
    app.add(main)

    return app
