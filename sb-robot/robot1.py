#!/usr/bin/env python3

# Runner file for robot	2019-09-03
# 
import os, sys
if sys.platform != 'win32':
	assert os.getuid() == 0, "root privilage is needed. run as sudo"

from signal import wait

from core.helpers 						import Configuration
from core.events						import Event

from drivecontroller.drivecontroller 	import (RobotController, 
												BTObserver)

APP_DIRECTORY 	= 'sb-robot'
DATA_DIRECTORY 	= os.path.relpath('data', APP_DIRECTORY)

CONFIG_FILE = 'config.json'
CONFIG_PATH = os.path.join(DATA_DIRECTORY, CONFIG_FILE)

config = Configuration.importConfig(CONFIG_PATH)

# 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 

controller 	= RobotController()
bluedot 	= BlueDot()
bt_observer = BTObserver()

controller.configure(config)

movedDot = Event('movedDotEvent')
pressedDot = Event('pressedDotEvent')
releasedDot = Event('releasedDotEvent')

bt_observer.register(movedDot, bt_observer.movedDot)
bt_observer.register(pressedDot, bt_observer.pressedDot)
bt_observer.register(releasedDot, bt_observer.releasedDot)

bluedot.set_when_moved(movedDot)
bluedot.set_when_pressed(pressedDot)
bluedot.set_when_released(releasedDot)

bluedot.wait_for_press()

while True:
	x = 1