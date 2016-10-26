""""Main Program of the PiWatch"""
import importlib
import os
import sys
from piwatch import *
import pygame

assert sys.version_info >= (3, 0)

debug_mode = "-d" in sys.argv
appsfolder = 'apps'
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + os.sep + appsfolder)
current_app = None
current_overlays = None
current_services = None
screen = None
main_variables = None
main_eventqueue = None
apps = {}
overlays = {}
services = {}

# Settings
screenres = (320, 240)  # Resolution of our TFT touchscreen
if not sys.platform in ['win32', 'win64']:
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.putenv('SDL_FBDEV', '/dev/fb1')
    os.putenv('SDL_MOUSEDRV', 'TSLIB')
    os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

if sys.version_info >= (3, 5):
    def load_module(name):
        """Load module for Python 3.5+"""
        spec = importlib.util.find_spec(name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
else:
    def load_module(name):
        """Load module for Python 3.3 and 3.4"""
        return importlib.machinery.SourceFileLoader(name, appsfolder + os.sep + name + '.py').load_module()


def start_app(appname, screen):
    global apps, current_app
    current_app = apps[appname]
    current_app.start(screen)


def start_service(service_name):
    global services, current_services
    current_services.append(services[service_name])


def start_overlay(overlay_name, screen):
    global overlays, current_overlays
    overlay = overlays[overlay_name]
    current_overlays.append(overlay)
    overlay.start(screen)


def load_apps_and_services():
    """Read .py files from the apps folder"""
    print('Loading apps...')
    _apps = {}
    _services = {}
    _overlays = {}
    for file in list(os.listdir(appsfolder)):
        if file.split('.')[-1] == 'py':
            appname = '.'.join(file.split('.')[:-1])
            print('  - ' + appname)
            app_module = load_module(appname)
            if hasattr(app_module, 'define_app'):
                app = app_module.define_app()
                _apps[app.name] = app
            if hasattr(app_module, 'define_overlay'):
                overlay = app_module.define_overlay()
                _overlays[overlay.name] = overlay
            if hasattr(app_module, 'define_services'):
                returned_service = app_module.define_services()
                if type(returned_service) is list or type(returned_service) is tuple:
                    for service in returned_service:
                        _services[service.name] = service
                else:
                    _services[returned_service.name] = returned_service

    if len(_apps) == 1:
        print(len(_apps), 'app loaded.')
    else:
        print(len(_apps), 'apps loaded.')
    if len(_overlays) == 1:
        print(len(_overlays), 'overlay loaded.')
    else:
        print(len(_overlays), 'overlays loaded.')
    if len(_services) == 1:
        print(len(_services), 'service loaded.')
    else:
        print(len(_services), 'services loaded.')
    print()
    return _apps, _services, _overlays


def handle_main_events(main_events):
    for event in main_events:
        if event.type == 'main start app':
            start_app(event.data, screen)
        elif event.type == 'main start service':
            start_service(event.data)
        elif event.type == 'main close service':
            for service in filter(lambda s: s.name == event.data, current_services):
                current_services.remove(service)
        elif event.type == 'main start overlay':
            start_overlay(event.data, screen)
        elif event.type == 'main close overlay':
            print("Closing:", event.data)
            for overlay in filter(lambda o: o.name == event.data, current_overlays):
                current_overlays.remove(overlay)
        elif event.type == 'main notification':
            if 'notification' not in (overlay.name for overlay in current_overlays):
                start_overlay('notification', screen)
            main_eventqueue.add(Event('notification', data=event.data))
        elif event.type == 'main get variable':
            main_eventqueue.add(Event('variable return', data=(event.data, main_variables[event.data])))
        elif event.type == 'main set variable':
            main_variables[event.data[0]] = event.data[1]
        elif event.type == 'main exit':
            sys.exit()
        else:
            print("Main event not recognised:", event)


def run():
    """
    Main function of the PiWatch
    """
    # PiWatch boot procedure
    global apps, services, overlays, current_app, current_services, current_overlays, screen, main_variables, main_eventqueue
    apps, services, overlays = load_apps_and_services()
    pygame.init()
    if sys.platform == 'linux' and not debug_mode:
        screen = pygame.display.set_mode(screenres, pygame.FULLSCREEN)
        pygame.mouse.set_visible(False)
    else:
        screen = pygame.display.set_mode(screenres)
    main_variables = {}
    main_eventqueue = Eventqueue()
    main_eventqueue.add(Event('boot'))

    current_services = [services['bluetooth service']]
    current_overlays = []

    fps = pygame.time.Clock()
    main_variables['fps'] = 0

    # boot apps and services
    start_app('bluetooth app', screen)
    start_overlay('fps counter', screen)
    start_overlay('bluetooth_overlay', screen)

    # mainloop
    while True:
        # events
        main_eventqueue.import_events(current_app, *current_services)
        main_eventqueue.add(Event('new frame', data=main_variables['fps']))
        events_for_main = filter(lambda e: e.type[:4] == 'main', main_eventqueue.events)
        handle_main_events(events_for_main)
        main_eventqueue.handle_events()
        main_eventqueue.broadcast(current_app, *(current_services + current_overlays))

        # fps counter
        fps.tick()
        try:
            main_variables['fps'] = int(fps.get_fps())
        except OverflowError:
            main_variables['fps'] = 'Infinity'

        # Draw
        screen.fill(current_app.bg_color)
        current_app.draw(screen)
        for overlay in current_overlays:
            overlay.draw(screen)

        pygame.display.flip()


# Call the main function
run()
