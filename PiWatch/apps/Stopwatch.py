from piwatch import *

def define_app():
    app = App(
        name='Stopwatch',
        bg_color=(63, 68, 84)
    )

    main = Activity(
        name='main'
    )

    clock = Clock()

    bttn_attrs = dict(
        Text.attributes,
        size=30,
        color=(0, 0, 0),
        padding=(30, 10)
    )

    bttn_start_pause = Text(
        bttn_attrs,
        message='start',
        bg_color=(69, 99, 232)
    )

    bttn_reset = Text(
        bttn_attrs,
        message='reset',
        bg_color=(255, 255, 255)
    )

    bttns = List(
        direction='right',
        position=('midbottom', 0, -40),
        children=[bttn_start_pause, bttn_reset],
        padding=50
    )

    main.add(bttns)
    app.add(main)
    return app