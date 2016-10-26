from piwatch import *


def define_app():
    app = App(
        name='fps counter'
    )

    main = Activity(
        name='main'
    )

    fps_counter = Text(
        position=('topleft', 0, 0),
        size=15
    )

    @app.event_listener('new frame')
    def new_frame(event):
        fps_counter.update(message=str(event.data))

    main.add(fps_counter)
    app.add(main)
    return app
