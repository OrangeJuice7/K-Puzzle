class Move(object):
	def __init__(self, state, direction):
		self.state = state
		self.direction = direction

	def get_state(self):
		return self.state