# standards
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import abc, math

from time 					import time, sleep

# package imports
if __name__ == '__main__':
	from ..events 	import (Event, 
							Observer)
	from ..helpers	import LEFT, RIGHT, ThreadPoolExecutorStackTraced

else:
	from core.events 	import (Event, 
								Observer)
	from core.helpers	import LEFT, RIGHT, ThreadPoolExecutorStackTraced


class DCMotor:
	def __init__(self, name, PINS, PWM_Frequecy = 200 ):
		if len(PINS) == 0:
			raise ValueError('no pins passed')

		self._pins		= {     'ENABLE' : PINS[0],
								'IN_1'   : PINS[1],
								'IN_2'   : PINS[2],
							}
		self._PWM_freq  = PWM_Frequecy	# Hz
		self._PWM_Obj 	= GPIO.PWM(self._pins.get('ENABLE'), self._PWM_freq)

		self.throttle   = 0     # %

	def drive_cw(self):
		self._PWM_Obj.start(self.throttle)
		# GPIO.PWM(self._pins['en'], self.throttle)
		GPIO.output(self._pins['IN_1'], True)
		GPIO.output(self._pins['IN_2'], False)

	def drive_ccw(self):
		self._PWM_Obj.start(self.throttle)
		# GPIO.PWM(self._pins['en'], self.throttle)
		GPIO.output(self._pins['IN_1'], False)
		GPIO.output(self._pins['IN_2'], True)

	#### TO BE TESTED
	# PWM or digitial?
	def set_idle(self):
		GPIO.output(self._pins['en'], False)


	def set_stop(self):
		self._PWM_Obj.stop()
		GPIO.output(self._pins['IN_1'], False)
		GPIO.output(self._pins['IN_2'], False)


class MotionController:
	def __init__(self):
		self._motors	= {	LEFT: None,
							RIGHT: None}
		self._looping = True
		self.command = None

		self._ThreadWorker = ThreadPoolExecutorStackTraced().__enter__()

	def configure(self, config):
		print('initializing hardware...')

		for pins in config['gpio']:
			if pins['type'][0] == GPIO.IN:
				GPIO.setup(pins['pins'], pins['type'][0], pins['type'][1])
			elif pins['type'][0] == GPIO.OUT:
				GPIO.setup(pins['pins'], pins['type'][0])

		self._motors[LEFT] = DCMotor(LEFT, config['gpio'][LEFT]['pins'])
		self._motors[RIGHT] = DCMotor(RIGHT, config['gpio'][RIGHT]['pins'])

		self._motors[LEFT].throttle = 100
		self._motors[RIGHT].throttle = 100

	def _forward(self):
		self._motors[LEFT].drive_cw()
		self._motors[RIGHT].drive_ccw()

	def _backward(self):
		self._motors[LEFT].drive_ccw()
		self._motors[RIGHT].drive_cw()

	def _start_check_pipeline(self, pipeline):
		print('MOTION: starting loop..', pipeline)
		while self._looping:
			sleep(0.05)
			if len(pipeline) > 1:
				print('MOTION: checked pipeline length')
				accel = pipeline[-1]['IMU']['accel']
			else:
				accel = (0, 0, 0)
			print('MOTION: found data:', accel)
			print('MOTION: looping')

			alpha = math.atan2(accel[0], accel[2])
			print(round(alpha, 3))

			if alpha >= 0:
				self._forward()
			elif alpha < 0:
				self._backward()

	
	def _stop_checking(self):
		self._looping = False

	def start(self, pipeline):
		self._ThreadWorker.submit(self._start_check_pipeline, pipeline)

	def stop(self):
		self._stop_checking()
		self._ThreadWorker.__exit__(None, None, None)
		print('MOTION: stopped')
		GPIO.cleanup()


class BTObserver(Observer):
	def __init__(self):
		super().__init__()

		self._BT_Interaction = None

	def movedDot(self, arg):
		print('moved')
	def releasedDot(self, arg):
		print('\n','released')
	def pressedDot(self, arg):
		print('pressed\n')

	# def getCommand(self):
	# 	return self.command.getCommand()

class Command(abc.ABC):
	def __init__(self):
		self.throttle = 0
		self.direction = 0

	@abc.abstractmethod
	def getThrottle(self, command):
		pass


if __name__ == '__main__':
	
	MyRobot = RobotController()
	print(MyRobot)


