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
Python, PyGame and the GPIO module. However, PyBluez must be
installed separately with the following commands:
```
sudo apt-get install python-bluez
sudo apt-get install libbluetooth-dev
sudo pip3 install pybluez
```

Furthermore, SDL could be version 2, which is incompatible with PyGame.
Make sure you have SDL 1.2

Clone from this GitHub repository and you should be ready to rock your
very own smartwatch.
```
git clone https://github.com/TertsDiepraam/PiWatch.git 
```

Use the guide on github repository of the the Android app to install it.

## Running
Make sure the raspberry pi is discoverable if you want to connect the
smartwatch to your Android device.

Enter the PiWatch directory **inside** this repository and run:
```
sudo python3 main.py
```

If you have no touchscreen, debug mode is recommended:
```
sudo python3 main.py -d
```

## Connecting to the Android device
Connecting the Android device to the smartphone is easy:
First, open the bluetooth app on the smartwatch. This app has a button
that says: `start server`. Touch it and watch the icon in the top right
corner of the screen: it will turn white.
On your Android device, open the app and touch `CONNECT`. Then grant all
the permissions. You should be set up now.