import os, sys, traceback
import RPi.GPIO as GPIO

from concurrent.futures import ThreadPoolExecutor

from core.configuration import load_config_file
# ++++++++++++++++++++++++++++
# constants
LEFT = 0
RIGHT = 1

config = load_config_file()

class IO():
	def __init__(self):
		self._pins = []
		self.event_status = False

		print('setting gpio pins')
		for pin in config['gpio']:
			if pin['type'][0] == GPIO.OUT:
				GPIO.setup(pin['pins'], pin['type'][0])
			elif pin['type'][0] == GPIO.IN:
				GPIO.setup(pin['pins'], pin['type'][0], pin['type'][1])

			if pin['name'] == 'BTN_CHANGE_MODE':
				self._button_id = pin['pins'][0]

			self._pins.append(pin['pins'])

	def _cb(self):
		print('button pressed')

	def wait_for_command(self, transition_method):
		GPIO.wait_for_edge(self._button_id, 
			GPIO.RISING, 
			bouncetime=config['core']['click_speed'])

		if callable(transition_method):
			transition_method()
		else:
			raise TypeError('transition not callable')

		return True

	def print_pipeline(self, pipeline):
		for entry in pipeline:
			print('time: ', entry.time, 'accel: ', entry.IMU['accel'])


class ThreadPoolExecutorStackTraced(ThreadPoolExecutor):

    def submit(self, fn, *args, **kwargs):
        """Submits the wrapped function instead of `fn`"""

        return super(ThreadPoolExecutorStackTraced, self).submit(
            self._function_wrapper, fn, *args, **kwargs)

    def _function_wrapper(self, fn, *args, **kwargs):
        """Wraps `fn` in order to preserve the traceback of any kind of
        raised exception

        """
        try:
            return fn(*args, **kwargs)
        except Exception:
            raise sys.exc_info()[0](traceback.format_exc())  # Creates an
                                                             # exception of the
                                                             # same type with the
                                                             # traceback as
                                                             # message


	# config_in = {
	# 	"core"	: {	"click_speed": 300},
	# 	"bt" 	: {	"devs":["OnePlus 6"],
	# 				"MAC": ["64:A2:F9:2F:6A:9B"]},
	# 	"motorGLOBAL":{	"f_PWM": 200,},
	# 	"gpio"	: [{ 	"name": "leftMotor",
	# 					"type": [GPIO.OUT],
	# 					"pins": [12, 20, 16]}, 
	# 				{ 	"name": "rightMotor",
	# 					"type": [GPIO.OUT],
	# 					"pins": [13, 26, 19]},
	# 				{ 	"name": "LED_STATUS_BT",
	# 					"type": [GPIO.OUT],
	# 					"pins": [14]},
	# 			    {	"name": "BTN_CHANGE_MODE",
    #   					"type": [GPIO.IN, GPIO.PUD_DOWN],
    #   					"pins": [15]}],
	# 	"IMU"	: { "settings_file" : "RTIMULib",
	# 				"IP"			: "127.0.0.2",
	# 				"PORT"			: 5005,
	# 				"slerpPower"	: 0.02
	# 				}
	# 			}

