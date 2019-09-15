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
		self.event_status = False

		self._button_id = 0

	def configure(self, config):
		print('setting gpio pins')
		for pin in config['gpio']:
			if len(pin['type']) > 1:
				GPIO.setup(pin['pins'], pin['type'])
			else:
				GPIO.setup(pin['pins'], pin['types'][0], pin['types'][1])

			if pin['name'] == 'BTN_CHANGE_MODE':
				self._button_id = config['gpio'].index(pin)

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
		GPIO.wait_for_edge(config['gpio'][self._button_id], 
			GPIO.FALLING, 
			bouncetime=300)

		transition_method()
		return 0



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
						"type": [GPIO.OUT, GPIO.PUD_UP],
						"pins": [12, 20, 16]}, 
					{ 	"name": "rightMotor",
						"type": [GPIO.OUT, GPIO.PUD_UP],
						"pins": [13, 26, 19]},
					{ 	"name": "LED_STATUS_BT",
						"type": [GPIO.OUT, GPIO.PUD_UP],
						"pins": [14]},
				    {	"name": "BTN_CHANGE_MODE",
      					"type": [GPIO.IN],
      					"pins": [15]}]}


	Configuration.exportConfig(config_in, os.path.join(DATA_DIRECTORY, CONFIG_FILE))
	c = Configuration.importConfig(os.path.join(DATA_DIRECTORY, CONFIG_FILE))
	print(c)
	
	
	# print(c == config_in)




