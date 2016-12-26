from piwatch import *


def define_overlay():
    overlay = Overlay(
        name='clock'
    )

    main = Activity(
        name='main'
    )

    clock = Clock(
        size=17,
        position=('topright', -25, 4)
    )

    @overlay.event_listener('started app Home')
    @overlay.event_listener('resumed app Home')
    def disappear(event):
        main.clear()

    @overlay.event_listener('closed app Home')
    def appear(event):
        if clock not in main.objects:
            main.add(clock)

    main.add(clock)
    overlay.add(main)
    return overlay
