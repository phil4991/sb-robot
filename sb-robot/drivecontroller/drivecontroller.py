# standards
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import abc

# modules
from core.events 	import Event, Observer # module not found! in init übernehmen?
from core.helpers	import LEFT, RIGHT
from bluedot 		import BlueDot

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


class RobotController:
	def __init__(self):
		self._motors	= {	LEFT: None,
							RIGHT: None}
		self._mode = None
		self.command = None

		self.DAQController 	= None


	def configure(self, config):

		if self.DAQController is not None:
			self.DAQController.configure(config)

		print('initializing hardware...')

		for pins in config['gpio']:
			if pins['type'][0] == GPIO.IN:
				GPIO.setup(pins['pins'], pins['type'][0], pins['type'][1])
			elif pins['type'][0] == GPIO.OUT:
				GPIO.setup(pins['pins'], pins['type'][0])


		self._motors[LEFT] = DCMotor(LEFT, config['gpio'][LEFT]['pins'])
		self._motors[RIGHT] = DCMotor(RIGHT, config['gpio'][RIGHT]['pins'])
	def close(self):
		GPIO.cleanup()
		
	def set_mode(self, mode):
		self._mode = mode


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

	def getCommand(self):
		return self.command.getCommand()

class Command(abc.ABC):
	def __init__(self):
		self.throttle = 0
		self.direction = 0

	@abc.abstractmethod
	def _getThrottle(self, command):
		pass


if __name__ == '__main__':
	
	MyRobot = RobotController()
	print(MyRobot)


