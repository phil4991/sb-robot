# daq module for all data aqisition and handling specific classes 2019-09-16
# 

# module imports
import abc, sys
from time 					import time, sleep
from threading 				import Thread, Lock
from collections 			import namedtuple, deque

from sensors 				import IMU

# package imports
# None


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

			self.DataPipeline.add_item(data_buf)

	def _stop_writing(self):
		self._loop_running = False

