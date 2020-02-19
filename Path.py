class Path(object):
	def __init__(self, moves):
		self.moves = moves

	def add_move(move):
		updated_moves = self.moves.copy()
		updated_moves.append(move)
		return Path(updated_moves)

	def get_recent_move():
		return self.moves[-1]

	def get_path_length():
		return len(self.moves)