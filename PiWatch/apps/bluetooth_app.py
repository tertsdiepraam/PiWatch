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
    @threaded
    def discover_devices(event):
        print('Discovering Devices')
        try:
            nearby_devices = bluetooth.discover_devices()
        except OSError:
            service.global_eventqueue.add(Event('bl no devices found'))
        else:
            return_value = []
            for bdaddr in nearby_devices:
                return_value.append(bluetooth.lookup_name(bdaddr))
                print('Done with Discovering')
                service.global_eventqueue.add(Event('bl devices discovered', data=return_value))

    return service


def define_app():
    app = App(
        name='bluetooth app'
    )

    discover_bttn = Text(
        message='Discover Devices',
        size=30,
        position=('midtop', 0, 10),
        bg_color=(50, 50, 50)
    )

    discovered_devices = List(
        position=('center', 0, 0),
    )
    discovered_devices.add(Text(message='No Discovered Devices'))

    @app.event_listener('mouse_down')
    def mouse_down_handler(event):
        if discover_bttn.check_collision(event.pos):
            app.global_eventqueue.add(Event('bl discover'))

    @app.event_listener('bl discovered')
    def bl_discovered(event):
        adapter = [str_to_text(string) for string in event.data]
        discovered_devices.clear()
        discovered_devices.add(*adapter)

    main = Activity(name='main')
    main.add(discover_bttn, discovered_devices)
    app.add(main)

    return app
