'''
Main Robot Code 2019-02-23


'''

import RPi.GPIO as GPIO
import sys

from time import sleep

global OUTPUT, INPUT
OUTPUT = GPIO.OUT
INPUT = GPIO.IN

class DCMotor:
	"""docstring for DCMotor"""


	def __init__(self, name, pinList):
		self._name = name
		self._pins = { 	'en'		: pinList[0],
						'in1'		: pinList[1],
						'in2'		: pinList[2],
					}

		GPIO.setup(pinList, OUTPUT)
		print(self._name, 'initialized ->', self._pins)


	def drive_cw(self):
		GPIO.output(self._pins['en'], True)
		GPIO.output(self._pins['in1'], True)
		GPIO.output(self._pins['in2'], False)


	def drive_ccw(self):
		GPIO.output(self._pins['en'], True)
		GPIO.output(self._pins['in1'], False)
		GPIO.output(self._pins['in2'], True)


	def idle(self):
		GPIO.output(self._pins['en'], False)


	def stop(self):
		GPIO.output(self._pins['en'], True)
		GPIO.output(self._pins['in1'], False)
		GPIO.output(self._pins['in2'], False)


def reset_pin(pins):
	print('\nreset pins')
	for number in pins:
		GPIO.output(number, False)






''' 
MAIN PROGRAM 



'''
if __name__ == '__main__':
	try:
		GPIO.setmode(GPIO.BCM)

		lDr = DCMotor(	name = 'leftDrive', 
						pinList = [
									21,		# enA
									16, 	# in1
									20,		# in2
									])
		rDr = DCMotor(	name = 'rightDrive',
						pinList = [
									26,		# enB
									19,		# in3
									13,		# in4
									])

		reset_pin([
			21, 16, 20,	# left motor
			26, 19, 13, # right motor
			])

		print('initialized')

		while True:
			lDr.drive_cw()
			rDr.drive_cw()
			print('drive cw')
			sleep(5)

			lDr.drive_ccw()
			rDr.drive_ccw()
			print('drive ccw')
			sleep(5)




	except KeyboardInterrupt:
		reset_pin([
			21, 16, 20,	# left motor
			26, 19, 13, # right motor
			])

	finally:
		GPIO.cleanup()



