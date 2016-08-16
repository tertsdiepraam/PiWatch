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
    mainclock = Clock(
        size=96,
    )

    textblock = Text(
        size=40,
        color=(0, 255, 255),
        position=('midbottom', 0, 0),
        message='Hello, World!')

    cursor = TextCursor(
        TextAttrs(),
        size=30,
        color=(255, 255, 255),
        position='midbottom',
        font="Times New Roman",
        message='O')

    # Activities
    main = Activity(name='main')
    main.add(mainclock, textblock, cursor)

    @main.event_listener('mouse_down')
    def settexttoBar():
        textblock.update('Hello, PiWatch!')

    # Add the activity to the app
    app.add(main)

    return app
