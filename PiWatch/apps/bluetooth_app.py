import bluetooth
import subprocess
import sys
from piwatch import *

self_sock = None
client_sock = None
client_address = None
abort_connection = False
connection_active = False


def define_services():
    service = Service(
        name='bluetooth service'
    )

    def bt_clean_up():
        global self_sock, client_sock, client_address, abort_connection, connection_active
        if self_sock: self_sock.close()
        if client_sock: client_sock.close()
        self_sock, client_sock = None, None
        abort_connection = False
        connection_active = False

    @service.event_listener('bt start rfcomm server')
    @threaded
    def start_rfcomm_server(event):
        """Starts a threaded RFCOMM server, which keeps listening
            to incoming data."""
        global client_sock, self_sock, abort_connection, connection_active
        if sys.platform == 'linux':
            code = subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
            if not code:
                print("ooowww yeah motherf*cker")
            else:
                print("Fuck you")
        connection_active = True
        self_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        port = 0
        data_size = 1024
        self_sock.bind(("", port))
        self_sock.listen(1)

        uuid = "bcfa2015-0e37-429b-8907-5b434f9b9093"
        bt_service_name = "PiWatch Android Connection Service"
        bluetooth.advertise_service(self_sock, bt_service_name,
                                    service_id=uuid,
                                    service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE])
        print("Advertising bt service: ", bt_service_name)

        try:
            global client_address
            client_sock, client_address = self_sock.accept()
        except OSError:
            if abort_connection:
                print('bt connection aborted')
                service.global_eventqueue.add(Event('bt connection aborted'))
            else:
                print('bt connection failed')
                service.global_eventqueue.add(Event('bt connection failed'))
            bt_clean_up()
        except:
            print('bt connection failed')
            service.global_eventqueue.add(Event('bt connection failed'))
            bt_clean_up()
        else:
            print("Accepted connection from ", client_address[0])
            service.global_eventqueue.add(Event('bt connection active', data=bluetooth.lookup_name(client_address[0])))
            try:
                client_sock.send("Hey There!")
                while True:
                    print(abort_connection)
                    data = client_sock.recv(data_size)
                    if data:
                        service.global_eventqueue.add(Event('bt data received', data=data))
                        client_sock.send(data)
                        print("Received bluetooth data: " + str(data))
            except:
                pass
            finally:
                bt_clean_up()
                service.global_eventqueue.add(Event('bt connection aborted'))

    @service.event_listener('bt abort connection')
    def abort_connection(event):
        print('Aborting connection')
        global abort_connection
        abort_connection = True
        if self_sock:
            self_sock.close()
        if client_sock:
            client_sock.close()

    @service.event_listener('bt data received')
    def send_notifications(event):
        info = event.data.decode("utf-8").split("|")
        if info[0] == 'notification posted':
            app = info[1].split(".")[1]
            title = info[2]
            text = info[3] if info[3] != 'null' else ""
            service.global_eventqueue.add(Event('main notification', data=[app, title, text]))

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
        if client_sock:
            print('sending string:', event.data)
            client_sock.send(event.data)
        else:
            print("bt send failed: No Connection")
            service.global_eventqueue.add(Event('bt send failed'))

    return service


def define_app():
    app = App(
        name='Bluetooth',
        icon='bluetooth.png'
    )
    main = Activity(
        name='main'
    )

    title = Text(
        message='Bluetooth Settings',
        size=30,
        position=('midtop', 0, 25)
    )

    status = Text(
        message='Not Connected',
        size=20,
        position=('midtop', 0, 70),
    )

    instructions = Text(
        message='Touch "start server"',
        size=20,
        position=('midtop', 0, 100)
    )

    server_bttn = Text(
        message='start server',
        size=30,
        position=('midbottom', 0, -50),
        bg_color=(0, 0, 70),
        padding=(30, 30)
    )

    def bttn_connection_active():
        global connection_active
        connection_active = True
        server_bttn.update(
            message='abort connection',
            bg_color=(70, 0, 0)
        )

    def bttn_connection_not_active():
        global connection_active
        connection_active = False
        server_bttn.update(
            message='start server',
            bg_color=(0, 0, 70)
        )

    @main.event_listener('mouse down')
    def mouse_down(event):
        global connection_active
        if server_bttn.check_collision(event.pos):
            if connection_active:
                app.global_eventqueue.add(Event('bt abort connection'))
            else:
                app.global_eventqueue.add(Event('bt start rfcomm server'))
                status.update(message='Waiting for connection')
                instructions.update(message='connect using the app')
                bttn_connection_active()

    @main.event_listener('bt connection active')
    def bt_connection_active(event):
        status.update(message="Connected to:")
        instructions.update(message=event.data)

    @main.event_listener('bt connection failed')
    def bt_connection_failed(event):
        status.update(message='Connection failed')
        instructions.update(message='try again')
        bttn_connection_not_active()

    @main.event_listener('bt connection aborted')
    def bt_connection_aborted(event):
        status.update(message='Connection aborted')
        instructions.update(message='Press button to try again')
        bttn_connection_not_active()

    main.add(title, status, instructions, server_bttn)
    app.add(main)

    return app
