"""module for all sensor specific classes 2019-11-03
"""

# module imports
import abc

from RTIMU 	    import Settings, RTIMU
from core.configuration import load_config_file

config = load_config_file()

class BasicSensor(abc.ABC):
	def __init__(self, name):
		self.name = name
		self.pollIntervall = 0
		self.interrupt_flag = True

	@abc.abstractmethod
	def configure(self, config):
		pass

	@abc.abstractmethod
	def read(self):
		pass


class IMU(BasicSensor):
	def __init__(self, name, settingsFile):
		super().__init__(name)

		self.IMU = RTIMU(Settings(settingsFile))
		print('settings file loaded succesfully from ', settingsFile)

		self.IMU_IP = None
		self.IMU_PORT = None


	def configure(self, config):
		imu_config = config['imu']

		self.IMU_IP = imu_config['ip']
		self.IMU_PORT = imu_config['port']

		print('initilizing IMU...')
		if not self.IMU.IMUInit():
			assert 0, 'IMU could not be initilized'

		self.IMU.setSlerpPower(imu_config['slerpPower'])  
		self.IMU.setGyroEnable(True)  
		self.IMU.setAccelEnable(True)  
		self.IMU.setCompassEnable(True) 

		self.pollIntervall = self.IMU.IMUGetPollInterval()
		print('set IMU pollintervall to ', self.pollIntervall)

	def read(self):
		if self.IMU.IMURead():
			data = self.IMU.getIMUData()
			print('IMU: got IMU data..')
			self.interrupt_flag = False
			return data
		else:
			print('IMU: reading IMU failed!')
			return -1


class WheelEncoder(BasicSensor):
	pass

class UltrasonicSensor(BasicSensor):
	pass
