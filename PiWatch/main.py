""""Main Program of the PiWatch"""
import importlib
import os
import sys

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

def load_apps():
    """Read .py files from the apps folder"""
    print('Loading apps...')
    apps = {}
    for file in list(os.listdir(appsfolder)):
        if file.split('.')[-1] == 'py':
            appname = '.'.join(file.split('.')[:-1])
            print('  - ' + appname)
            spec = importlib.util.find_spec(appname)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            app = module.define_app()
            apps[app.name] = app
    if len(apps) == 1:
        print(len(apps),'app loaded.\n')
    else:
        print(len(apps), 'apps loaded.\n')
    return apps


def run():
    """
    Main function of the PiWatch
    """
    # PiWatch boot procedure
    apps = load_apps()
    pygame.init()
    if sys.platform == 'linux':
        screen = pygame.display.set_mode(screenres, pygame.FULLSCREEN)
        pygame.mouse.set_visible(False)
    else:
        screen = pygame.display.set_mode(screenres)
    eventqueue = Eventqueue()

    current_app = apps['home']
    print("Starting app: " + current_app.name)
    current_app.start(screen)

    current_services = []

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
        eventqueue.handle_events()
        eventqueue.broadcast(current_app, *current_services)

        # Draw
        screen.fill(current_app.bg_color)
        current_app.draw(screen)

        # fps counter
        fps.tick()
        try:
            fpstext.update(str(int(fps.get_fps())))
        except OverflowError:
            fpstext.update("Infinity, BITCH!!!!!")
        fpstext.draw(screen)

        pygame.display.flip()


# Call the main function
run()
