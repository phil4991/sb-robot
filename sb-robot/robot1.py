#!/usr/bin/env python3

# Runner file for robot	2019-09-03
# 
import os, sys
if sys.platform != 'win32':
	assert os.getuid() == 0, "root privilage is needed. run as sudo"

from bluedot import BlueDot
from core.helpers 						import Configuration, IO
from core.events						import Event
from core.state							import StateMachine

from drivecontroller.drivecontroller 	import (RobotController, BTObserver)
from DAQ.daq_suite						import DAQController

APP_DIRECTORY 	= 'sb-robot'
DATA_DIRECTORY 	= os.path.relpath('data', APP_DIRECTORY)

CONFIG_FILE = 'config.json'
CONFIG_PATH = os.path.join(DATA_DIRECTORY, CONFIG_FILE)

config = Configuration.importConfig(CONFIG_PATH)

# 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 

controller 	 = RobotController()
bluedot 	 = BlueDot()
bt_observer  = BTObserver()
statemachine = StateMachine()
io_module	 = IO()
daq_controller = DAQController()

controller.configure(config)
io_module.configure(config)
daq_controller.configure(config)

movedDot = Event('movedDotEvent')
pressedDot = Event('pressedDotEvent')
releasedDot = Event('releasedDotEvent')

bt_observer.register(movedDot, bt_observer.movedDot)
bt_observer.register(pressedDot, bt_observer.pressedDot)
bt_observer.register(releasedDot, bt_observer.releasedDot)

bluedot.when_moved = movedDot.fire
bluedot.when_pressed = pressedDot.fire
bluedot.when_released = releasedDot.fire

statemachine.init()

if io_module.wait_for_command(statemachine.enable_control):
	print('starting daq...')
	daq_controller.start()

	daq_controller.exit()
	io_module.print_pipeline(daq_controller.pipeline._buffer[:5])

print('program exit in state {}'.format(statemachine.state))
