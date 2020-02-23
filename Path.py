class Path(object):
	def __init__(self, moves):
		self.moves = moves

	def add_move(self, move):
		updated_moves = self.moves.copy()
		updated_moves.append(move)
		return Path(updated_moves)

	def get_recent_move(self):
		# print("panjang kontol")
		# print(len(self.moves))
		return self.moves[-1]

	def get_path_length(self):
		return len(self.moves)

	def remove_first(self):
		updated_moves = self.moves.copy()
		updated_moves.pop(0)
		return Path(updated_moves)

	def __lt__(self, other):
		return True