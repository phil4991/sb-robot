# daq module for all sensor specific classes 2019-09-16
# 

import abc
from RTIMU import Settings, RTIMU

class BasicSensor(abc.ABC):
	def __init__(self):
		self.pollIntervall = None

	@abc.abstractmethod
	def configure(self):
		pass
		
class DAQController():
	def __init__(self):
		self._sensors = {
		}

	def configure(self, config):
		pass

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

		self.pollIntervall = self.IMU.IMUGetPollInterval()
		print('set pollintervall to ', self.pollintervall)

class WheelEncoder(BasicSensor):
	pass
