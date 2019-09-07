import json, os

class Configuration:
	def importConfig(path):
		with open(path, 'r') as f:
			cfg = json.load(f)

		return cfg

	def exportConfig(cfg, outfile):
		with open(outfile, 'w') as out:
			json.dump(cfg, out, indent=2)

		return 0

	def getModuleConfig(self):
		pass

if __name__ == '__main__':
	APP_DIRECTORY 	= 'sb-robot/sb-robot'
	DATA_DIRECTORY 	= os.path.relpath('data', APP_DIRECTORY)

	CONFIG_FILE = 'config.json'
	config_in = {
		"core"	: {	"name":"core"},
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
						"pins": [14]}]}


	# Configuration.exportConfig(config_in, os.path.join(DATA_DIRECTORY, CONFIG_FILE))
	c = Configuration.importConfig(os.path.join(DATA_DIRECTORY, CONFIG_FILE))

	print(c)
	# print(c == config_in)




