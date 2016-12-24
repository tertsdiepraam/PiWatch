# PiWatch
The PiWatch project: A smartwatch built on a Raspberry Pi 2 using python 3 and pygame.

Dependencies:
 - Python 3.x
 - Pygame
 - SDL
 - pybluez
 - RPi.GPIO module

Current Features:
 - Load custom apps
 - Draw text
 - Draw image
 - Create groups of components
 - Event handling

## Installation:
Make sure you have Python 3.5+.
Make sure your device is Bluetooth compatible.

The NOOBS installation of Rasbian should have the correct versions of
Python, SDL, PyGame and the GPIO module. However, PyBluez must be
installed separately with the following commands:
```
sudo apt-get install python-bluez
sudo apt-get install libbluetooth-dev
sudo pip3 install pybluez
```

Clone from this GitHub repository and you should be ready to rock your
very own smartwatch.
```
git clone https://github.com/TertsDiepraam/PiWatch.git 
```

## Running
Enter the PiWatch directory **inside** this repository and run:
```
sudo python3 main.py
```

If you have no touchscreen, debug mode is recommended:
```
sudo python3 main.py -d
```