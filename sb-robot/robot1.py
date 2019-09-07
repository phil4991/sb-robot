#!/usr/bin/env python3

# Runner file for robot	2019-09-03
# 
import os, sys
if sys.platform != 'win32':
	assert os.getuid() == 0, "root privilage is needed. run as sudo"


from core.helpers 						import Configuration
from core.state							import State
from core.events						import Event

from drivecontroller.drivecontroller 	import (RobotController, 
												BTCallback, 
												RobotEventObserver)

APP_DIRECTORY 	= 'sb-robot/sb-robot'
DATA_DIRECTORY 	= os.path.relpath('data', APP_DIRECTORY)

CONFIG_FILE = 'config.json'
CONFIG_PATH = os.path.join.(DATA_DIRECTORY, CONFIG_FILE)

config = Configuration.importConfig(CONFIG_PATH)

# 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 

MyRobot = RobotController()


MyRobot.configure(config)
MyRobot.BT.wait_for_press()
print('pressed')
