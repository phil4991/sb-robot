# daq module for all sensor specific classes 2019-09-16
# 

import abc, sys
from time import time, sleep
from RTIMU import Settings, RTIMU

class BasicSensor(abc.ABC):
	def __init__(self):
		self.pollIntervall = 0
		self.interrupt_flag = 0

	@abc.abstractmethod
	def configure(self):
		pass

	@abc.abstractmethod
	def read(self):
		pass
		
class DAQController():
	def __init__(self):
		self._sensors = {
		}
		self.current_pollIntervall = 0
		self._loop_running = False


	def configure(self, config):
		self._sensors['IMU'] = IMU(config['IMU']['settings_file'])

		print('setting maximum polling time..')
		maximum = 0		# huge value to start
		for name, sensor in self._sensors.items():
			if sensor.pollIntervall < maximum:
				maximum = sensor.pollIntervall
		if maximum != 0:
			self.current_pollIntervall = maximum

		return 0


	def getData(self):
		self._loop_running = True
		timer = time()
		while self._loop_running:
			print(time)
			sleep(self.current_pollIntervall/1000.0)



class IMU(BasicSensor):
	def __init__(self, settingsFile):
		super().__init__()
		self.settings = Settings(settingsFile)
		print('settings file loaded succesfully from ', settingsFile)

		self.IMU = RTIMU(self.settings)
		self.IMU_IP = None
		self.IMU_PORT = None


	def configure(self, config):
		imu_config = config['IMU']

		self.IMU_IP = imu_config['IP']
		self.IMU_PORT = imu_config['PORT']

		self.IMU.setSlerpPower(imu_config['slerpPower'])  
		self.IMU.setGyroEnable(True)  
		self.IMU.setAccelEnable(True)  
		self.IMU.setCompassEnable(False) 

		try:
			print('initilizing IMU...')
			self.IMU.IMUInit()
		except Exception as e:
			raise e
			sys.exit(1)

		self.pollIntervall = self.IMU.IMUGetPollInterval()
		print('set IMU pollintervall to ', self.pollintervall)

class WheelEncoder(BasicSensor):
	pass

class UltrasonicSensor(BasicSensor):
	pass
