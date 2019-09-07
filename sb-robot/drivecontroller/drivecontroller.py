# standards
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# modules
from core.events 	import Event, Observer # module not found! in init übernehmen?
from core.state 	import State
from bluedot 		import BlueDot


class Controller():
	def configure(self, config):
		pass

class RobotEventObserver(Observer):
	def State_changed_Cb(self):
		pass



class DCMotor:
	def __init__(self, name, PINS = [0, 0, 0], PWM_Frequecy = 200 ):
		if all(PINS) == 0:
			raise ValueError('no pins passed')
		try:
			GPIO.setup(PINS, GPIO.OUT)
		except Exception as e:
			raise e
			print('GPIO SETUP FAILED')

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
	def idle(self):
		GPIO.output(self._pins['en'], False)


	def stop(self):
		self._PWM_Obj.stop()
		GPIO.output(self._pins['IN_1'], False)
		GPIO.output(self._pins['IN_2'], False)


class RobotController(Controller):
	def __init__(self):

		self._leftMotor 	= None
		self._rightMotor 	= None

		self.BT 			= BlueDot()
		self.EventHandler 	= None
		self.DAQController 	= None

		self.State 			= None


	def configure(self, config):

		if self.DAQController is not None:
			self.DAQController.configure(config)

		print('initializing hardware...')

		for pins in config['gpio']:
			if pins['type'] is 'IN':
				GPIO.setup(self._INPUT, GPIO.IN)
			elif pins['type']	is 'OUT':
				GPIO.setup(pins['pins'], GPIO.OUT)
			else:
				print('Warning! unrecognized pintype')	

		self._leftMotor = DCMotor('leftMotor', config['gpio'][0]['pins'])
		self._rightMotor = DCMotor('rightMotor', config['gpio'][1]['pins'])



		

class BTCallback:
	def movedDot():
		pass
	def releasedDot():
		pass
	def pressedDot():
		pass


if __name__ == '__main__':
	
	MyRobot = RobotController()
	print(MyRobot)
