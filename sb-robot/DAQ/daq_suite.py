# daq module for all sensor specific classes 2019-09-16
# 

import abc, sys
from time 					import time, sleep
from RTIMU 					import Settings, RTIMU
from threading 				import Thread, Lock
from concurrent.futures 	import ThreadPoolExecutor

class BasicSensor(abc.ABC):
	def __init__(self, name):
		self.name = name
		self.pollIntervall = 0
		self.interrupt_flag = 0

		self.pipeline = None

	@abc.abstractmethod
	def configure(self, config, pipeline):
		pass

	@abc.abstractmethod
	def read(self):
		pass

class DataPipeline:
	def __init__(self):
		self._buffer = list()

		self._producer_lock = Lock()
		self._consumer_lock = Lock()

	def add_item(self, item):
		self._producer_lock.aquire()
		self._buffer.append(item)
		self._consumer_lock.release()

	def get_item(self):
		if len(self._buffer) > 0:
			self._consumer_lock.aquire()
			
			data = self._buffer[0]
			del self._buffer[0]

			self._producer_lock.release()
			return data
		else:
			return None

		
class DAQController():
	def __init__(self):
		self._sensors = dict()
		self.current_pollIntervall = 0
		self._loop_running = False

		self._ThreadWorker = ThreadPoolExecutor().__enter__()
		self.pipeline = DataPipeline()

	def configure(self, config):
		self._sensors['IMU'] = IMU('IMU', '../data/' + config['IMU']['settings_file'])

		print('setting maximum polling time..')
		maximum = 0		# huge value to start
		for name, sensor in self._sensors.items():
			if sensor.pollIntervall < maximum:
				maximum = sensor.pollIntervall
		if maximum != 0:
			self.current_pollIntervall = maximum
		print('DAQ configuration done')

	def start(self):
		self._ThreadWorker.submit(self.write_to_pipeline)

	def stop(self):
		self._ThreadWorker.__exit__(None, None, None)

	def _check_buffer(self, buffer):
		# +1 -> time column
		if len(self._sensors.values())+1 == len(buffer):
			return True
		else:
			return False

	def write_to_pipeline(self):
		self._loop_running = True
		t_0 = round(time(), 3)
		data_buf = dict(['time', *self._sensors.keys()])

		reading = False
		while self._loop_running:
			if not reading:
				t = round(time(), 3)
				sleep(self.current_pollIntervall/1000.0)
				
				data_buf = dict(['time', *self._sensors.keys()])
				data_buf['time'] = t - t0
				reading = True

			if self._sensors['IMU'].interrupt_flag:
				data_buf['IMU'] = self._sensors['IMU'].read()

			if self._check_buffer(data_buf):
				self.pipeline.add_item(data_buf)

	def stop_writing(self):
		self._loop_running = False



class IMU(BasicSensor):
	def __init__(self, name, settingsFile):
		super().__init__(name)
		self.settings = Settings(settingsFile)
		print('settings file loaded succesfully from ', settingsFile)

		self.IMU = RTIMU(self.settings)
		self.IMU_IP = None
		self.IMU_PORT = None


	def configure(self, config, pipeline=None):
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

		if pipeline is not None:
			self.pipeline = pipeline

	def read(self):
		if self.IMU.IMURead():
			data = self.IMU.getIMUData()
			self.interrupt_flag = False
			return data



class WheelEncoder(BasicSensor):
	pass

class UltrasonicSensor(BasicSensor):
	pass
