"""Events 2019-08-11
event structure for controllers
 
class overview
	- Handler
	- Event	
"""


class Observer():
	_observers = []
	_registered_names = []
	def __init__(self):
		self._observers.append(self)
		
		# event names and corresponding callbacks referenced in dict
		self._database = {}

	def register(self, eventObj, callback):
		if callable(callback) and eventObj.name not in Observer._registered_names:
			Observer._registered_names.append(eventObj.name)
			self
			self._database[eventObj.name] = callback
		else:
			ValueError('Error! registered callback is not callable or name is already used')

	def unregister(self, eventObj):
		if eventObj.name in self._database.keys():
			del self._database[eventObj.name]
		else:
			print('Warning! event not found. ')


class Event():
	def __init__(self, name):
		self.name = name

	def fire(self, arg = None):
		for observer in Observer._observers:
			if self.name in observer._database: 
				if arg is None:
					observer._database[self.name]()
				else:
					observer._database[self.name](arg)

			



# ###########################################################################
# TEST CODE
# ###########################################################################
if __name__ == '__main__':

	# Test!
	class Room(Observer):
		def __init__(self):
		    print("Room is ready.")
		    super().__init__() # Observer's init needs to be called
		def someone_arrived(self, who):
		    print(who + " has arrived!")
		def someone_left(self):
		    print('someone left!')



	room = Room()
	room1 = Room()
	e1 = Event('ArriveEvent')
	e2 = Event('LeaveEvent')
	print(room._observers)

	room.register(e1,  room.someone_arrived)
	room.register(e2,  room.someone_left)
	print('events registered ', *room._database.items())
	
	


	e1.fire('test')
	e2.fire()
