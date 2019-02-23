'''
Main Robot Code 2019-02-23


'''

import RPi.GPIO as GPIO
import sys


GPIO.setmode(GPIO.BOARD)

OUTPUT = GPIO.OUT
INPUT = GPIO.IN


class DCMotor:
	"""docstring for DCMotor"""
	_name = 'noName'
	_pins = { 	'enableA'	: None,
				'in1'		: None,
				'in2'		: None,
	}

	def __init__(self, name):
		self._name = name

		#declare all output pins
		for name, pin in self._pins.items():
			GPIO.setup(pin, OUTPUT)

	def set_name(self, name):
		self._name = name

	def set_pins(self, pin_list):
		if type(pin_list) is list:
			i = 0
			for name, number in self._pins.items():
				self._pins[name] = pin_list[i]
				i += 1
		else:
			print('Define pins in a list!\n')
			sys.exit()



	def drive_cw(self):
		GPIO.output(self._pins['enableA'], True)
		GPIO.output(self._pins['in1'], True)
		GPIO.output(self._pins['in2'], False)

	def drive_ccw(self):
		GPIO.output(self._pins['enableA'], True)
		GPIO.output(self._pins['in1'], False)
		GPIO.output(self._pins['in2'], True)

	def idle(self):
		GPIO.output(self._pins['enableA'], False)

	def stop(self):
		GPIO.output(self._pins['enableA'], True)
		GPIO.output(self._pins['in1'], False)
		GPIO.output(self._pins['in2'], False)



		

def reset_pin(pins):
	print('reset pins')
	for number in pins:
		GPIO.output(number, False)


def setup():
	print('test')

def loop():
	print('loop')



''' 
MAIN PROGRAM 


'''
setup()

try:
	while True:
	loop()
except KeyboardInterrupt:
	pass



