from piwatch import *


def define_bapp():
    app = App(
        name='example'
    )
    main = Activity(
        name='main'
    )
    text_1 = Text(
        message="Click me!",
        size=30
    )

    @app.event_listener("mouse up")
    def mouse_up(event):
        if text_1.check_collision(event.pos):
            text_1.update(size=text_1.size*1.2)

    @app.event_listener("resumed app example")
    def resume(event):
        text_1.update(size=30)

    main.add(text_1)
    app.add(main)
    return app
