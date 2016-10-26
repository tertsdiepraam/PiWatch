from piwatch import *

def define_overlay():
    overlay = Overlay(
        name='bluetooth_overlay'
    )

    main = Activity(
        name='main'
    )

    bt_icon = Image(
        filename=overlay.folder + '0.png',
        size_x=16,
        position=('topright', -5, 5)
    )

    @overlay.event_listener('bt start rfcomm server')
    def start_rfcomm_server(event):
        bt_icon.update(filename=overlay.folder + '1.png')

    @overlay.event_listener('bt connection active')
    def connection_active(event):
        bt_icon.update(filename=overlay.folder + '2.png')

    @overlay.event_listener('bt connection failed')
    def connection_failed(event):
        bt_icon.update(filename=overlay.folder + '0.png')

    @overlay.event_listener('bt connection aborted')
    def connection_aborted(event):
        bt_icon.update(filename=overlay.folder + '0.png')

    main.add(bt_icon)
    overlay.add(main)
    return overlay
