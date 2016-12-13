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
        bg_color=(150, 150, 150, 100)
    )

    @app.event_listener('started app {}'.format(app.name))
    def boot(event):
        status = start_app
        app.global_eventqueue.add('main get variable', data='bt_connected')

    @app.event_listener('mouse down')
    def mouse_down(event):
        if bttn.check_collision(event.pos):
            take_picture = 1
            bttn.update(filename=app.folder + 'bttn2.png')
            app.global_eventqueue.add('main get variable', data='bt_connected')

    @app.event_listener('variable return')
    def variable(event):
        if event.data[0] == 'bt_connected':
            connected = event.data[1]
            if connected:
                if status != take_picture:
                    app.eventqueue.add('bt send', data='camera remote open')
                else:
                    app.eventqueue.add('bt send', data='camera take picture')
            else:
                info.update(message='Not connected to a smartphone')

    @app.event_listener('mouse up')
    def mouse_up(event):
        bttn.update(filename=app.folder + 'bttn.png')

    main.add(bttn, info)
    app.add(main)
    return app