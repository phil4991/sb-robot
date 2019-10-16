# statemachine module 2019-09-12
# 	
from transitions import Machine

class StateMachine():
	states = [	'power_on', 
				'wait_for_command', 
				'balancing', 
				'bt_controlled',
				'failed',
				'power_off']

	def __init__(self):
		self.machine = Machine(
							model=self,
							states=StateMachine.states,
							initial=StateMachine.states[0])

		self.machine.add_transition(trigger='init', source=StateMachine.states[0], dest='wait_for_command')

		# transitions from state wait_for_command
		self.machine.add_transition(trigger='enable_control', source=StateMachine.states[1], dest='balancing')
		self.machine.add_transition(trigger='shutdown', source=StateMachine.states[1], dest='power_off')

		# transitions from state balancing
		self.machine.add_transition(trigger='disable_control', source=StateMachine.states[2], dest='wait_for_command')
		self.machine.add_transition(trigger='enable_bt', source=StateMachine.states[2], dest='bt_controlled')
		self.machine.add_transition(trigger='shutdown', source=StateMachine.states[2], dest=StateMachine.states[-1])
		

		# transitions from state bt_controlled
		self.machine.add_transition(trigger='disable_bt', source=StateMachine.states[3], dest='balancing')
		self.machine.add_transition(trigger='shutdown', source=StateMachine.states[3], dest=StateMachine.states[-1])

		def function(self):
			pass
		


if __name__ == '__main__':
	statemachine = StateMachine()

	#  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	# TESTCASES
	print('testing base states..')
	if statemachine.states[0] == 'power_on':
		print('test for init state successful')


	if statemachine.states[-1] == 'power_off':
		print('test for exit state successful')


