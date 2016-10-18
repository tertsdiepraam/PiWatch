appsfolder = 'apps'


def define_app():
    # App object and settings
    app = App(
        name='home',
        icon=None,
        bg_color=(0, 0, 0))

    # Components
    mainclock = Clock(
        size=96,
        position=('center', 0, -25)
    )

    maindate = Date(
        position=('center', 0, 30),
        size=25
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
    main.add(mainclock, maindate, cursor)

    @main.event_listener('mouse_down')
    def mouse_event(event):
        if mainclock.check_collision(event.pos):
            pass
        if hello_text.check_collision(event.pos):
            pass
        if other_text.check_collision(event.pos):
            pass

    # Add the activity to the app
    app.add(main)

    return app
