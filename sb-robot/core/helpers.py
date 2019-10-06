import json, os
import RPi.GPIO as GPIO

# ++++++++++++++++++++++++++++
# constants
LEFT = 0
RIGHT = 1

# classes
class Configuration:
	def importConfig(path):
		with open(path, 'r') as f:
			cfg = json.load(f)

		return cfg

	def exportConfig(cfg, outfile):
		with open(outfile, 'w') as out:
			json.dump(cfg, out, indent=4)

		return 0

	def configure_all(self, classes, config):
		pass

class IO():
	def __init__(self):
		self._pins = []
		self.event_status = False

		self._button_id = 0

	def configure(self, config):
		print('setting gpio pins')
		for pin in config['gpio']:
			if pin['type'][0] == GPIO.OUT:
				GPIO.setup(pin['pins'], pin['type'][0])
			elif pin['type'][0] == GPIO.IN:
				GPIO.setup(pin['pins'], pin['type'][0], pin['type'][1])

			if pin['name'] == 'BTN_CHANGE_MODE':
				self._button_id = pin['pins'][0]

			self._pins.append(pin['pins'])

		self._click_speed = config['core']['click_speed']

		# print('setting io events..')
		# GPIO.add_event_detect(pin[self._button_id]['pin'][0], 
		# 						GPIO.FALLING, callback=IO._cb, 
		# 						bouncetime=300)
		return 0

	def _cb(self):
		print('button pressed')

	def wait_for_command(self, transition_method):
		GPIO.wait_for_edge(self._button_id, 
			GPIO.RISING, 
			bouncetime=self._click_speed)

		transition_method()
		return True

	def print_pipeline(self, pipeline):
		for val in pipeline[1:]:
			print('time: ', val['time'], 'accel: ', val['IMU']['accel'])



if __name__ == '__main__':
	APP_DIRECTORY 	= 'sb-robot'
	DATA_DIRECTORY 	= os.path.relpath('data', APP_DIRECTORY)

	CONFIG_FILE = 'config.json'
	config_in = {
		"core"	: {	"click_speed": 300},
		"bt" 	: {	"devs":["OnePlus 6"],
					"MAC": ["64:A2:F9:2F:6A:9B"]},
		"motorGLOBAL":{	"f_PWM": 200,},
		"gpio"	: [{ 	"name": "leftMotor",
						"type": [GPIO.OUT],
						"pins": [12, 20, 16]}, 
					{ 	"name": "rightMotor",
						"type": [GPIO.OUT],
						"pins": [13, 26, 19]},
					{ 	"name": "LED_STATUS_BT",
						"type": [GPIO.OUT],
						"pins": [14]},
				    {	"name": "BTN_CHANGE_MODE",
      					"type": [GPIO.IN, GPIO.PUD_DOWN],
      					"pins": [15]}],
		"IMU"	: { "settings_file" : "RTIMULib",
					"IP"			: "127.0.0.2",
					"PORT"			: 5005,
					"slerpPower"	: 0.02
					}
				}


	Configuration.exportConfig(config_in, os.path.join(DATA_DIRECTORY, CONFIG_FILE))
	c = Configuration.importConfig(os.path.join(DATA_DIRECTORY, CONFIG_FILE))
	print(c)
	
	
	# print(c == config_in)




