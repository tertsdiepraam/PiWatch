import os
import time

from pi_utils import *

appsfolder = 'apps'


def define_app():
    # App object and settings
    app = App(
        name='home',
        icon=None,
        bg_color=(0, 0, 0))

    appfolder = 'apps' + os.sep + app.name + os.sep

    # Components
    # mainclock = Clock(
    #     size=96
    # )

    hello_text = Text(
        size=40,
        color=(0, 255, 255),
        position=('midbottom', 0, 0),
        message='Hello, World!'
    )

    other_text = Text(
        size=40,
        color=(0,255,255),
        position=('midtop',0,0),
        message='bla'*6
    )

    cursor = TextCursor(
        TextAttrs(),
        size=30,
        color=(255, 255, 255),
        position='midbottom',
        font="Times New Roman",
        message='O'
    )

    # Activities
    main = Activity(name='main')
    main.add(hello_text, other_text, cursor)

    @main.event_listener('mouse_down')
    @return_event(app)
    def mouse_event(event):
        if mainclock.check_collision(event.pos):
            print('Starting thread yippie(counter=4)')
            yippie(counter=4)
            print('Starting thread yippie(4)')
            yippie(4)
        if hello_text.check_collision(event.pos):
            return Event('blub')
        if other_text.check_collision(event.pos):
            print('Starting thread yippie()')
            yippie()

    @app.event_listener('blub')
    def blub_event(event):
        hello_text.update(time_to_str(event.timestamp))

    @thread
    def yippie(counter=1):
        for i in range(counter):
            print(i, 'Yippie Ki-Yay Motherfucker!')
            time.sleep(0.1)
        print('done')

    # Add the activity to the app
    app.add(main)

    return app
