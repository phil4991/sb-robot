#!/usr/bin/env python3
"""Runner file for robot	2019-09-03
"""

import os, sys
if sys.platform != 'win32':
	assert os.getuid() == 0, "root privilage is needed. run as sudo"

from bluedot 				import BlueDot
from core.helpers 			import IO
from core.events			import Event
from core.state				import StateMachine

from motion.motion_suite 		import (MotionController, BTObserver)
from daq.daq_suite			import DAQController

APP_DIRECTORY 	= 'sb-robot'
DATA_DIRECTORY 	= os.path.relpath('data', APP_DIRECTORY)


bluedot 	 = BlueDot()
bt_observer  = BTObserver()
statemachine = StateMachine()
io_module	 = IO()
daq_controller = DAQController()
motion_controller = MotionController()
motion_controller.DataPipeline = daq_controller.DataPipeline

motion_controller.configure()
daq_controller.configure()

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
	print('MAIN: starting daq...')
	daq_controller.start()
	motion_controller.start()
	print('MAIN: executing...')

print('MAIN: waiting for command..')
if io_module.wait_for_command(statemachine.disable_control):
	daq_controller.stop()
	motion_controller.stop()
	io_module.print_pipeline(daq_controller.DataPipeline._daq_buffer)

print('MAIN: program exit in state {}'.format(statemachine.state))
