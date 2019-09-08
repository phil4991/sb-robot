# Events 2019-08-11
# event structure for controllers
# 
# class overview
# 	- Handler
# 	- Event


class Observer():
	_observers = []
	def __init__(self):
		self._observers.append(self)
		
		# event names and corresponding callbacks referenced in dict
		self._database = {}

	def register(self, eventObj, callback):
		if iscallable(callback):
			self._database[eventObj.name] = callback
		else:
			ValueError('Error! registered event is not callable')

	def unregister(self, eventObj):
		if eventObj in self._events:
			i = self._events.index(eventObj)

			del self._events[i]
			del self._callbacks[i]
		else:
			print('Warning! event not found. ')


class Event():
	_nEvents = 0
	def __init__(self, name):
		self._nEvents += 1
		self.name = name

	def fire(self, arg = None):
		for i, observer in enumerate(Observer._observers):
			if self._nEvents == -1:
				assert 0, "no handler found"
			elif self._nEvents == i:
				if arg != None:
					print('called w\ arg ', observer._callbacks[i])
					observer._callbacks[i](arg)
				else:
					print('called w\o arg ', observer._callbacks[i])
					observer._callbacks[i]()



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
	print('events registered ', room._events)
	
	


	e1.fire('test')
	e2.fire()
