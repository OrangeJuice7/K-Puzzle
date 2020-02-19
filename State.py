class State(object):
	def __init__(self, grid, is_initial, manhattan_distance_heuristic):
		self.grid = grid;
		self.is_initial = is_initial;
		self.manhattan_distance_heuristic = manhattan_distance_heuristic

	def calculate_heuristic():
		return self.manhattan_distance_heuristic

	def get_grid_size():
		return len(self.grid)