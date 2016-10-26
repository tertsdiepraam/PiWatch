from piwatch import *


def define_overlay():
    overlay = Overlay(
        name='fps counter'
    )

    main = Activity(
        name='main'
    )

    fps_counter = Text(
        position=('topleft', 0, 0),
        size=15
    )

    @overlay.event_listener('new frame')
    def new_frame(event):
        fps_counter.update(message=str(event.data))

    main.add(fps_counter)
    overlay.add(main)
    return overlay
