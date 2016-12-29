from piwatch import *
start_app = 0
take_picture = 1
status = 0

def define_app():
    app = App(
        name='Camera'
    )

    main = Activity(
        name='main'
    )

    bttn = Image(
        filename=app.folder + 'bttn.png',
    )

    info = Text(
        message='',
        visible=False,
        bg_color=(100, 100, 150)
    )

    @app.event_listener('started app {}'.format(app.name))
    def boot(event):
        app.global_eventqueue.add('bt send', data='camera remote open')
        bttn.update(
            visible=True
        )

    @app.event_listener('mouse down')
    def mouse_down(event):
        if bttn.check_collision(event.pos):
            bttn.update(filename=app.folder + 'bttn2.png')
            app.global_eventqueue.add('bt send', data='camera take picture')

    @app.event_listener('bt send failed')
    def failed(event):
        info.update(
            message='Not connected to a smartphone',
            visible=True,
            padding=20
        )
        bttn.update(
            visible=False
        )

    @app.event_listener('mouse up')
    def mouse_up(event):
        bttn.update(filename=app.folder + 'bttn.png')

    main.add(bttn, info)
    app.add(main)
    return app
