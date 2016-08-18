import bluetooth
from pi_utils import *

def define_services():

    service = Service(
        name='bluetooth service'
    )

    @service.event_listener('boot')
    def boot_bluetooth(event):
        pass

    @service.event_listener('bl discover')
    @thread
    def discover_devices(event):
        print('Discovering Devices')
        nearby_devices = bluetooth.discover_devices()
        return_value = ""
        for bdaddr in nearby_devices:
            return_value += bluetooth.lookup_name(bdaddr) + '\n'
            print('Done with Discovering')
            service.global_eventqueue.add(Event('bl devices discovered', msg=return_value))

    return service

def define_app():

    app = App(
        name='bluetooth app'
    )

    discover_bttn = Text(
        message='Discover Devices',
        size=30,
        position=('midtop', 0, 10),
        bg_color=(50,50,50)
    )

    discovered_devices = Text(
        message='No Devices Discovered',
        size=20,
        position=('midtop', 0, 45)
    )

    @app.event_listener('bl devices discovered')
    def bl_discovered_handler(event):
        discovered_devices.update(event.msg)

    @app.event_listener('mouse_down')
    def mouse_down_handler(event):
        if discover_bttn.check_collision(event.pos):
            print('Adding Event bl discover')
            app.global_eventqueue.add(Event('bl discover'))

    main = Activity(name='main')
    main.add(discover_bttn, discovered_devices)
    app.add(main)

    return app