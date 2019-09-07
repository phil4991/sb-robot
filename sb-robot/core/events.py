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
		self._events = []
		self._callbacks = []

	def register(self, eventObj, callback):
		self._events.append(eventObj)
		self._callbacks.append(callback)

	def unregister(self, eventObj):
		# filter?
		if eventObj in self._events:
			i = self._events.index(eventObj)

			del self._events[i]
			del self._callbacks[i]
		else:
			print('Warning! event not found. ')


class Event():
	_nEvents = -1
	def __init__(self, name):
		self._nEvents += 1
		self.name = name

	def fire(self, arg):
		for i, observer in enumerate(Observer._observers):
			if self._nEvents == -1:
				assert 0, "no handler found"
			elif self._nEvents == i:
				print('called ', observer._callbacks[i])
				observer._callbacks[i](arg)



# ###########################################################################
# TEST CODE
# ###########################################################################
if __name__ == '__main__':

	# Test!
	class Room(Handler):
		def __init__(self):
		    print("Room is ready.")
		    Handler.__init__(self) # Observer's init needs to be called
		def someone_arrived(self, who):
		    print(who + " has arrived!")



	room = Room()
	room1 = Room()
	e1 = Event('ArriveEvent')

	room.listen(e1,  room.someone_arrived)
	print(room._events)


	e1.fire('test')