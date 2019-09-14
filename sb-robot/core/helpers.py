import json, os
import RPi.GPIO as GPIO

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

	def configure(self, config):

		for pin in config['gpio']:
			if pin['type'] == 'OUT':
				pin_type = GPIO.OUT
			elif pin['type'] == 'IN':
				pin_type = GPIO.IN

			GPIO.setup(pin['pins'], pin_type)
			self._pins.append(pin['pins'])

		self._click_speed = config['core']['click_speed']

		return 0

	def wait_for_command(self):
		

		GPIO.read(x)

if __name__ == '__main__':
	APP_DIRECTORY 	= 'sb-robot/sb-robot'
	DATA_DIRECTORY 	= os.path.relpath('data', APP_DIRECTORY)

	CONFIG_FILE = 'config.json'
	config_in = {
		"core"	: {	"click_speed": 0.3},
		"bt" 	: {	"devs":["OnePlus 6"],
					"MAC": ["64:A2:F9:2F:6A:9B"]},
		"motorGLOBAL":{	"f_PWM": 200,},
		"gpio"	: [{ 	"name": "leftMotor",
						"type": "OUT",
						"pins": [12, 20, 16]}, 
					{ 	"name": "rightMotor",
						"type": "OUT",
						"pins": [13, 26, 19]},
					{ 	"name": "StatusLED_BT",
						"type": "OUT",
						"pins": [14]},
				    {	"pins": [15],
    					"name": "BTN_CHANGE_MODE",
      					"type": "IN"}]}


	Configuration.exportConfig(config_in, os.path.join(DATA_DIRECTORY, CONFIG_FILE))
	c = Configuration.importConfig(os.path.join(DATA_DIRECTORY, CONFIG_FILE))
	print(c)
	
	
	# print(c == config_in)




