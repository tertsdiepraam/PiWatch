""""Main Program of the PiWatch"""
import importlib
import os
import sys

assert sys.version_info >= (3,0)

import pygame

appsfolder = 'apps'
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + os.sep + appsfolder)
from pi_utils import *

# Settings
screenres = (320, 240)  # Resolution of our TFT touchscreen
if sys.platform in ['win32', 'win64']:
    openappcommand = 'python'
else:
    openappcommand = 'python3'
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.putenv('SDL_FBDEV', '/dev/fb1')
    os.putenv('SDL_MOUSEDRV', 'TSLIB')
    os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + os.sep + appsfolder)

if sys.version_info >= (3,5):
    def load_module(name):
        """Load module for Python 3.5+"""
        spec = importlib.util.find_spec(name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
else:
    def load_module(name):
        """Load module for Python 3.3 and 3.4"""
        return importlib.machinery.SourceFileLoader(name, appsfolder).load_module()

def load_apps_and_services():
    """Read .py files from the apps folder"""
    print('Loading apps...')
    apps = {}
    services = {}
    for file in list(os.listdir(appsfolder)):
        if file.split('.')[-1] == 'py':
            appname = '.'.join(file.split('.')[:-1])
            print('  - ' + appname)
            app_module = load_module(appname)
            if hasattr(app_module, 'define_app'):
                app = app_module.define_app()
                apps[app.name] = app
            if hasattr(app_module, 'define_services'):
                returned_service = app_module.define_services()
                if type(returned_service) is list or type(returned_service) is tuple:
                    for service in returned_service:
                        services[service.name] = service
                else:
                    services[returned_service.name] = returned_service

    if len(apps) == 1:
        print(len(apps), 'app loaded.\n')
    else:
        print(len(apps), 'apps loaded.\n')
    return apps, services


def run():
    """
    Main function of the PiWatch
    """
    # PiWatch boot procedure
    apps, services = load_apps_and_services()
    pygame.init()
    if sys.platform == 'linux':
        screen = pygame.display.set_mode(screenres, pygame.FULLSCREEN)
        pygame.mouse.set_visible(False)
    else:
        screen = pygame.display.set_mode(screenres)
    main_eventqueue = Eventqueue()
    main_eventqueue.add(Event('boot'))

    current_app = apps['bluetooth app']
    print("Starting app: " + current_app.name)
    current_app.start(screen)

    current_services = []
    current_services.append(services['bluetooth service'])

    fps = pygame.time.Clock()
    fpstext = Text(
        TextAttrs(),
        position='topleft',
        size=15
    )
    fpstext.setup(screen)

    # mainloop
    while True:
        # events
        main_eventqueue.import_events(current_app, *current_services)
        main_eventqueue.handle_events()
        main_eventqueue.broadcast(current_app, *current_services)

        # Draw
        screen.fill(current_app.bg_color)
        current_app.draw(screen)

        # fps counter
        fps.tick()
        try:
            fpstext.update(message=str(int(fps.get_fps())))
        except OverflowError:
            fpstext.update(message="Infinity, BITCH!!!!!")
        fpstext.draw(screen)

        pygame.display.flip()


# Call the main function
run()
