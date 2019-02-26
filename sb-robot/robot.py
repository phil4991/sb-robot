'''
Main Robot Code 2019-02-23


'''

import RPi.GPIO	as GPIO
import sys

from time 		import sleep
from bluedot 	import BlueDot
from signal 	import pause

global OUTPUT, INPUT, controllerName, controllerMAC
OUTPUT = GPIO.OUT
INPUT = GPIO.IN

controllerName = 'OnePlus 6'
controllerMAC =  '64:A2:F9:2F:6A:9B' #'1C:AF:05:22:FE:43'

class DCMotor:
	"""docstring for DCMotor"""

	def __init__(self, name, pinList):
		self._name = name
		self._pins = { 	'en'		: pinList[0],
						'in1'		: pinList[1],
						'in2'		: pinList[2],
					}

		self.speed = 0		# %
		self._freq = 100 	# Hz

		GPIO.setup(pinList, OUTPUT)
		self._p = GPIO.PWM(self._pins['en'], self._freq)
		print(self._name, 'initialized ->', self._pins)



	def drive_cw(self):
		self._p.start(self.speed)
		# GPIO.PWM(self._pins['en'], self.speed)
		GPIO.output(self._pins['in1'], True)
		GPIO.output(self._pins['in2'], False)


	def drive_ccw(self):
		self._p.start(self.speed)
		# GPIO.PWM(self._pins['en'], self.speed)
		GPIO.output(self._pins['in1'], False)
		GPIO.output(self._pins['in2'], True)

	#### TO BE TESTED
	# PWM or digitial?
	def idle(self):
		GPIO.output(self._pins['en'], False)


	def stop(self):
		GPIO.output(self._pins['en'], True)
		GPIO.output(self._pins['in1'], False)
		GPIO.output(self._pins['in2'], False)

	def setSpeed(self, speed):
		# set PWM duty cycle
		self.speed = speed





def reset_pin(pins):
	print('\nreset pins')
	for number in pins:
		GPIO.output(number, False)


def move(pos):
    if pos.top:
        print(pos.distance, 'forward')
    elif pos.bottom:
        print(pos.distance, 'back')
    elif pos.left:
      	print(pos.distance, 'left')
    elif pos.right:
        print(pos.distance, 'rigth')

def stop():
    print('stop')

def show_percentage(pos):
    horizontal = ((pos.x + 1) / 2)
    vertical = ((pos.y + 1)/2)

    hPerc = round(horizontal * 100, 2)
    vPerc = round(vertical * 100, 2)
    print("H: {}%".format(horizontal))
    print("V: {}%".format(vertical))



''' 
MAIN PROGRAM 



'''
if __name__ == '__main__':
	try:
		print('\n##################')
		print('setting up hardware')
		GPIO.setmode(GPIO.BCM)

		lDr = DCMotor(	name = 'leftDrive', 
						pinList = [
									12,		# enA
									20, 	# in1
									16,		# in2
									])
		rDr = DCMotor(	name = 'rightDrive',
						pinList = [
									13,		# enB
									26,		# in3
									19,		# in4
									])

		reset_pin([
			12, 20, 16,	# left motor
			13, 26, 19  # right motor
			])

		print('\n###############')
		print('establish connection with controller')
		bd = BlueDot()




		print('\n###############')
		print('robot setup done!')

		while True:

			# bd.when_pressed = move
			# bd.when_moved = move
			# bd.when_released = stop

			bd.when_moved = show_percentage

			pause()

			# # lDr.setSpeed(50)
			# # rDr.setSpeed(50)

			# # lDr.drive_cw()
			# # rDr.drive_cw()
			# print('drive cw')
			# sleep(5)

			# # lDr.setSpeed(100)
			# # rDr.setSpeed(100)

			# # lDr.drive_ccw()
			# # rDr.drive_ccw()

			# print('drive ccw')
			# sleep(5)

	except KeyboardInterrupt:
		reset_pin([
			12, 20, 16,	# left motor
			13, 26, 19 # right motor
			])

	finally:
		GPIO.cleanup()



