# daq module for all sensor specific classes 2019-09-16
# 

import abc, sys
from time 					import time, sleep
from RTIMU 					import Settings, RTIMU
from threading 				import Thread, Lock
from collections 				import namedtuple, deque

# package imports
if __name__ == '__main__':
	from ..helpers 	import ThreadPoolExecutorStackTraced
else:
	from core.helpers 	import ThreadPoolExecutorStackTraced

class BasicSensor(abc.ABC):
	def __init__(self, name):
		self.name = name
		self.pollIntervall = 0
		self.interrupt_flag = True

	@abc.abstractmethod
	def configure(self, config, pipeline):
		pass

	@abc.abstractmethod
	def read(self):
		pass


class DataPipeline:
	def __init__(self):
		self._buffer = deque(maxlen=5)

		self._producer_lock = Lock()
		self._consumer_lock = Lock()
		self._consumer_lock.acquire()


	def add_item(self, item):
		print('PIPELINE: about to add an item')
		self._producer_lock.acquire()

		self._buffer.append(item)
		if len(self._buffer) > 5:
			self._buffer.popleft()
			print('PIPELINE: deleted buffer value!')

		self._consumer_lock.release()

	def get_item(self):
		if self._consumer_lock.acquire(blocking=False):
			if self._buffer:
				data = self._buffer[-1]
				self._producer_lock.release()
				return data
			else:
				self._producer_lock.release()
				return None
		print('PIPELINE: tried to get an item')
		return None


class DAQController():
	def __init__(self):
		self._sensors = dict()
		self.current_pollIntervall = 0
		self._loop_running = False

		self._thread = Thread(target=self._write_to_pipeline, daemon=True)
		self.DataPipeline = DataPipeline()

	def configure(self, config):
		self._sensors['IMU'] = IMU('IMU', '../data/' + config['IMU']['settings_file'])
		self._sensors['IMU'].configure(config)
		print('setting maximum polling time..')
		minimum = 1000		# huge value to start
		for name, sensor in self._sensors.items():
			print(sensor.name, ' ----> ', sensor.pollIntervall)
			if sensor.pollIntervall < minimum:
				minimum = sensor.pollIntervall
		if minimum != 0:
			self.current_pollIntervall = minimum
		print('DAQ configuration done')


	def start(self):
		print('starting aquisition thread...')
		self._thread.start()

	def stop(self):
		self._stop_writing()
		print('stopped aquisition thread')

	def _write_to_pipeline(self):
		self._loop_running = True
		t_0 = round(time(), 3)

		print('starting loop...')
		print('sensors: ', self._sensors)
		data_buf = namedtuple('DataEntry', ['time', *self._sensors.keys()])

		while self._loop_running:
			print('DAQ: looping..')
			t = round(time(), 3)
			sleep((self.current_pollIntervall+8)/1000.0)

			data_buf.time = round(t - t_0, 3)
			data_buf.IMU = self._sensors['IMU'].read()

			self.pipeline.add_item(data_buf)


	def _stop_writing(self):
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

		print('initilizing IMU...')
		if not self.IMU.IMUInit():
			assert 0, 'IMU could not be initilized'

		self.IMU.setSlerpPower(imu_config['slerpPower'])  
		self.IMU.setGyroEnable(True)  
		self.IMU.setAccelEnable(True)  
		self.IMU.setCompassEnable(True) 

		self.pollIntervall = self.IMU.IMUGetPollInterval()
		print('set IMU pollintervall to ', self.pollIntervall)

		if pipeline is not None:
			self.pipeline = pipeline

	def read(self):
		if self.IMU.IMURead():
			data = self.IMU.getIMUData()
#			print('IMU: got IMU data..')
			self.interrupt_flag = False
			return data
		else:
#			print('IMU: reading IMU failed!')
			return -1



class WheelEncoder(BasicSensor):
	pass

class UltrasonicSensor(BasicSensor):
	pass
