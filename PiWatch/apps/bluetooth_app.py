import bluetooth
from pi_utils import *

self_sock = None
client_sock = None


def define_services():
    service = Service(
        name='bluetooth service'
    )

    @service.event_listener('bt start rfcomm server')
    @threaded
    def start_rfcomm_server(event):
        """Starts a threaded RFCOMM server, which keeps listening
            to incoming data."""
        global client_sock
        global self_sock
        self_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        port = 0
        data_size = 1024
        self_sock.bind(("", port))
        self_sock.listen(1)

        uuid = "bcfa2015-0e37-429b-8907-5b434f9b9093"
        bt_service_name = "PiWatch Android Connection Server"
        bluetooth.advertise_service(self_sock, bt_service_name,
                                    service_id=uuid,
                                    service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE])
        print("Advertising bt service: ", bt_service_name)

        try:
            client_sock, client_address = self_sock.accept()
        except:
            print('Bluetooth Error: Closing socket')
            print()
            client_sock.close()
            self_sock.close()
        else:
            print("Accepted connection from ", client_address)
            while True:
                data = client_sock.recv(data_size)
                if data:
                    service.global_eventqueue.add(Event('Bt Data Received', data=data))
                    client_sock.send(data)
                    print("Received bluetooth data: " + str(data))
                    service.global_eventqueue.add(Event('main start home'))
            self_sock.close()
            client_sock.close()

    @service.event_listener('bt discover')
    @threaded
    def discover_devices(event):
        print('Discovering Devices')
        try:
            nearby_devices = bluetooth.discover_devices()
        except OSError:
            print('No devices found')
            service.global_eventqueue.add(Event('bt no devices found'))
        else:
            return_value = []
            for bdaddr in nearby_devices:
                return_value.append(bluetooth.lookup_name(bdaddr))
                print('Done with Discovering')
                service.global_eventqueue.add(Event('bt discovered', data=return_value))

    @service.event_listener('bt send')
    def send_bt_message(event):
        print('sending string:', event.data)
        client_sock.send(event.data)

    return service


def define_app():
    app = App(
        name='bluetooth app'
    )
    main = Activity(
        name='main'
    )

    discover_bttn = Text(
        message='Discover Devices',
        size=30,
        position=('midtop', 0, 10),
        bg_color=(50, 50, 50),
    )

    server_bttn = Text(
        message='Start server',
        size=30,
        position=('midbottom', 0, -10),
        bg_color=(50, 50, 50)
    )

    discovered_devices = List(
        position=('midtop', 0, 50),
    )

    discovered_devices.add(Text(message='No Discovered Devices'))

    @main.event_listener('mouse_down')
    def mouse_down_handler(event):
        if discover_bttn.check_collision(event.pos):
            app.global_eventqueue.add(Event('bt discover'))
        if server_bttn.check_collision(event.pos):
            app.global_eventqueue.add(Event('bt start rfcomm server'))

    @app.event_listener('bt discovered')
    def bt_discovered(event):
        adapter = [str_to_text(string) for string in event.data]
        discovered_devices.clear()
        discovered_devices.add(*adapter)

    main.add(discover_bttn, server_bttn, discovered_devices)
    app.add(main)

    return app
