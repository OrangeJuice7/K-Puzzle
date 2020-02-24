from heapq import heappush
from heapq import heappop

'''
informed_search is a method that defines the general procedure
of doing an informed search from the state to the goal. The function
takes in an initial state, as well as the goal state. A state is represented
as a 2D array. The function returns the
sequence of moves to solve the puzzle. It will return unsolvable.
'''

def informed_search(initial, goal):
	moves = _initialize_list()
	visited_states = {}
	initial = tuple(map(tuple, initial))
	if _is_solvable(initial):
		MDH_sum_beginning = calculate_manhattan_beginning(initial)
		# path = _run_astar(initial_state, goal, visited_states)
		path = _run_astar(initial, goal, visited_states, moves)
		# path = _remove_sort_key(path)
		# path = _remove_start_node(path)
		# _add_moves(moves, path)
		return path[3]
		
	else:
		_mark_unsolvable(moves)
		
	return moves

'''
_run_astar is the internal method to run the A* search. It takes in the initial
state, the goal state, as well as the set of visited states.

We maintain a priority queue that sort the path based on 
heuristics. And explore the next state with lowest expected cost.

Each entry of the priority queue is a tuple (heuristic_sort_key, path)
Each path is a list of tuples (next 2D state, the move to achieve next state)

By default, Python priority queue sort the tuple based on the first 
element of that tuple.

Evaluation function 
	= current length of the path + Manhattan distance of each tile from its proper position

When the goal state is reached, we return the path from source to goal.

'''

def _run_astar(initial, goal, visited_states, moves):
	source = (0, initial, 0, moves)
	pq = []
	heappush(pq, source)

	while (len(pq) != 0):
		pq_node = heappop(pq)
		# state = _get_most_recent_state(pq_node[1])
		state = pq_node[1]
		# print("ini state")
		# print(state)
		# if _is_reached(state.grid, goal):
		# 	return pq_node

		if _is_reached(state, goal):
			return pq_node

		x, y = _locate_blank(state)

		if _is_moved_down(x, state):
			_move_down(state, x, y, visited_states, pq, pq_node, pq_node[2], pq_node[3])

		if _is_moved_right(y, state):
			_move_right(state, x, y, visited_states, pq, pq_node, pq_node[2], pq_node[3])

		if _is_moved_up(x, state):
			_move_up(state, x, y, visited_states, pq, pq_node, pq_node[2], pq_node[3])

		if _is_moved_left(y, state):
			_move_left(state, x, y, visited_states, pq, pq_node, pq_node[2], pq_node[3])

		# mark the current state as visited
		# visit = tuple(map(tuple, state.grid))
		# visit = tuple(map(tuple, state))
		# print("ini visit")
		# print(visit)
		visited_states[state] = 1


def _heuristic_sum(previous_state, current_state, direction, x, y):
	if direction == "down":
		number = previous_state[x-1][y]
		length = len(previous_state)
		real_x_coordinate_of_number = (number-1) // length
		real_y_coordinate_of_number = (number-1) % length
		current_state.manhattan_distance_heuristic = previous_state.manhattan_distance_heuristic \
		- distance(real_x_coordinate_of_number, real_y_coordinate_of_number, x-1, y) \
		+ distance(real_x_coordinate_of_number, real_y_coordinate_of_number, x, y)

	if direction == "right":
		number = previous_state.grid[x][y-1]
		real_x_coordinate_of_number = (number-1) // previous_state.get_grid_size()
		real_y_coordinate_of_number = (number-1) % previous_state.get_grid_size()
		current_state.manhattan_distance_heuristic = previous_state.manhattan_distance_heuristic \
		- distance(real_x_coordinate_of_number, real_y_coordinate_of_number, x, y-1) \
		+ distance(real_x_coordinate_of_number, real_y_coordinate_of_number, x, y)

	if direction == "up":
		number = previous_state.grid[x+1][y]
		real_x_coordinate_of_number = (number-1) // previous_state.get_grid_size()
		real_y_coordinate_of_number = (number-1) % previous_state.get_grid_size()
		current_state.manhattan_distance_heuristic = previous_state.manhattan_distance_heuristic \
		- distance(real_x_coordinate_of_number, real_y_coordinate_of_number, x+1, y) \
		+ distance(real_x_coordinate_of_number, real_y_coordinate_of_number, x, y)

	if direction == "left":
		number = previous_state.grid[x][y+1]
		real_x_coordinate_of_number = (number-1) // previous_state.get_grid_size()
		real_y_coordinate_of_number = (number-1) % previous_state.get_grid_size()
		current_state.manhattan_distance_heuristic = previous_state.manhattan_distance_heuristic \
		- distance(real_x_coordinate_of_number, real_y_coordinate_of_number, x, y+1) \
		+ distance(real_x_coordinate_of_number, real_y_coordinate_of_number, x, y)


	# # the total distance between every misplaced tile and its expected position
	
	# Fill in as desired!

def _heuristic_sum_old(current_state):
	# n = current_state.get_grid_size()
	# total = 0

	# for i in range(0, n):
	# 	for j in range(0, n):
	# 		num = current_state.grid[i][j]
	# 		if num == 0:
	# 			continue
	# 		# offset = current pos - expected pos
	# 		disx = abs(i - (num - 1) // n)
	# 		disy = abs(j - (num - 1) % n)
	# 		total = total + disx + disy

	n = len(current_state)
	total = 0

	for i in range(0, n):
		for j in range(0, n):
			num = current_state[i][j]
			if num == 0:
				continue
			# offset = current pos - expected pos
			disx = abs(i - (num - 1) // n)
			disy = abs(j - (num - 1) % n)
			total = total + disx + disy
	return total

def _swap(state, nx, ny, ox, oy):
	# transform = list(map(list, state.grid))
	transform = list(map(list, state))
	temp = transform[ox][oy]
	transform[ox][oy] = transform[nx][ny]
	transform[nx][ny] = temp
	
	res = tuple(map(tuple, transform))
	return res


def _locate_blank(state):
	# find the coordinates of the blank cell (0)
	# in the puzzle grid

	# for i in range(0, state.get_grid_size()):
	# 	for j in range(0, state.get_grid_size()):
	# 		if state.grid[i][j] == 0:
	# 			return i, j

	for i in range(0, len(state)):
		for j in range(0, len(state[0])):
			if state[i][j] == 0:
				return i, j

	raise ValueError("Error: no blank cell exists!")


def _is_reached(state, goal):
	# check whether the current state is equal
	# to the goal state
	# state = list(map(list, state))
	for i in range(0, len(state)):
		for j in range(0, len(state[0])):
			if (state[i][j] != goal[i][j]): 
				return False

	return True


def _is_solvable(state):
	# If k is odd, the puzzle is solvable if there are even number
	# of inversion pairs; otherwise, it is not solvable

	# Else if k is even, the puzzle is solvable if the blank tile is
	# on the odd row and having an even inversion, or the blank tile is
	# on the even row and having an odd inversion

	inv_count = 0
	blank_row = -1
	# flattent the array from 2D into 1D
	flat = []
	for i in range(0, len(state)):
		for j in range(0, len(state[0])):
			if (state[i][j]) != 0:
				flat.append(state[i][j])
			else:
				blank_row = len(state) - i

	# count inversion pairs
	for m in range(0, len(flat)):
		for n in range(m, len(flat)):
			if (flat[m] and flat[n] and flat[m] > flat[n]):
				inv_count += 1

	if (len(state) % 2 == 1 or blank_row % 2 == 1):
		return inv_count % 2 == 0

	else:
		return inv_count % 2 == 1

'''
_mark_unsolvable is an internal method to mark that the puzzle is not
unsolvable. It takes in a sequence of moves in form of list, and append
the unsolvable mark to the list.
'''

def _mark_unsolvable(moves):
	moves.append("UNSOLVABLE")

'''
_initialize_list is an internal method to abstract the list creation.
'''

def _initialize_list():
	return []

'''
_remove_sort_key is an internal method to remove the sort_key after doing
the A* search. It takes in the result of A* search, and returns the path
to reach the goal state. The result of A* search is in form of (sort_key, path).
'''

def _remove_sort_key(path):
	return path[1]

'''
_remove_start_node is an internal method to remove the start node.
'''

def _remove_start_node(path):
	return path.remove_first()

'''
_add_moves adds all the moves from the A* search to the original list.
Each move is in form (next_state, next_move)
'''

def _add_moves(moves, path):
	for move in path.moves:
		moves.append(move.direction)

'''
_create_move creates the state, with the corresponding move. It takes in a state
and the move that is taken. It returns a Move object with the corresponding action that
has been taken.
'''

def _create_move(state, direction):
	return Move(state, direction)

'''
_create_path creates a Path object. It takes in a Move object as the initial move.
'''

def _initialize_path(initial_move):
	return Path([initial_move])

'''
_get_most_recent_state gets the most recent state from a path.
'''

def _get_most_recent_state(path):
	return path.get_recent_move().get_state()

'''
_is_moved_down checks whether there exists a tile that can be moved down.
'''

def _is_moved_down(x, state):
	# return 0 <= (x-1) < state.get_grid_size()
	return 0 <= (x-1) < len(state)

'''
_is_moved_up checks whether there exists a tile that can be moved up.
'''

def _is_moved_up(x, state):
	# return (x+1) < state.get_grid_size()
	return 0 <= (x+1) < len(state)

'''
_is_moved_left checks whether there exists a tile that can be moved left.
'''

def _is_moved_left(y, state):
	# return (y+1) < state.get_grid_size()
	return (y+1) < len(state[0])
'''
_is_moved_right checks whether there exists a tile that can be moved right.
'''

def _is_moved_right(y, state):
	# return 0 <= (y-1) < state.get_grid_size()
	return 0 <= (y-1) < len(state[0])

'''
_move_down moves the tile down to the blank tile.
'''

def distance(x1, y1, x2, y2):
	return abs(x1-x2) + abs(y1 - y2)

def _move_down(state, x, y, visited_states, pq, pq_node, length, moves):
	down = _swap(state, x-1, y, x, y)
	# if down.grid not in visited_states:
	# 	current_path = pq_node[1]
	# 	# _heuristic_sum(state, down, "down", x,y)
	# 	heuristic_value = _heuristic_sum_old(down)
	# 	down.manhattan_distance_heuristic = heuristic_value
	# 	current_path = current_path.add_move(Move(down, "DOWN"))
	# 	# print("kontol bawah")
	# 	# print(down.grid)
	# 	new_node = (current_path.get_path_length() + down.manhattan_distance_heuristic, current_path)
	# 	heappush(pq, new_node)
	if down not in visited_states:
		current_path = pq_node[1]
		# _heuristic_sum(state, down, "down", x,y)
		heuristic_value = _heuristic_sum_old(down)
		# print("kontol bawah")
		# print(down.grid)
		new_moves = list(moves)
		new_moves.append("DOWN")
		new_node = (length + heuristic_value, down, length + 1, new_moves)
		heappush(pq, new_node)

'''
_move_up moves the tile up to the blank tile.
'''

def _move_up(state, x, y, visited_states, pq, pq_node, length, moves):
	up = _swap(state, x+1, y, x, y)
	# if up.grid not in visited_states:
	# 	current_path = pq_node[1]
	# 	# _heuristic_sum(state, up, "up", x, y)
	# 	heuristic_value = _heuristic_sum_old(up)
	# 	up.manhattan_distance_heuristic = heuristic_value
	# 	current_path = current_path.add_move(Move(up, "UP"))
	# 	# print("kontol atas")
	# 	# print(up.grid)
	# 	new_node = (current_path.get_path_length() + up.manhattan_distance_heuristic, current_path)
	# 	heappush(pq, new_node)

	if up not in visited_states:
		current_path = pq_node[1]
		# _heuristic_sum(state, down, "down", x,y)
		heuristic_value = _heuristic_sum_old(up)
		# print("kontol bawah")
		# print(down.grid)
		new_moves = list(moves)
		new_moves.append("UP")
		new_node = (length + heuristic_value, up, length + 1, new_moves)
		heappush(pq, new_node)


'''
_move_right moves the tile right to the blank tile.
'''

def _move_right(state, x, y, visited_states, pq, pq_node, length, moves):
	right = _swap(state, x, y-1, x, y)
	# if right.grid not in visited_states:
	# 	current_path = pq_node[1]
	# 	# _heuristic_sum(state, right, "right", x, y)
	# 	heuristic_value = _heuristic_sum_old(right)
	# 	right.manhattan_distance_heuristic = heuristic_value
	# 	current_path = current_path.add_move(Move(right, "RIGHT"))
	# 	# print("kontol kanan")
	# 	# print(right.grid)
	# 	new_node = (current_path.get_path_length() + right.manhattan_distance_heuristic, current_path)
	# 	heappush(pq, new_node)

	if right not in visited_states:
		current_path = pq_node[1]
		# _heuristic_sum(state, down, "down", x,y)
		heuristic_value = _heuristic_sum_old(right)
		# print("kontol bawah")
		# print(down.grid)
		new_moves = list(moves)
		new_moves.append("RIGHT")
		new_node = (length + heuristic_value, right, length + 1, new_moves)
		heappush(pq, new_node)


'''
_move_left moves the tile left to the blank tile.
'''

def _move_left(state, x, y, visited_states, pq, pq_node, length, moves):
	left = _swap(state, x, y+1, x, y)
	# if left.grid not in visited_states:
	# 	current_path = pq_node[1]
	# 	# _heuristic_sum(state, left, "left", x, y)
	# 	heuristic_value = _heuristic_sum_old(left)
	# 	left.manhattan_distance_heuristic = heuristic_value
	# 	current_path = current_path.add_move(Move(left, "LEFT"))
	# 	# print("kontol kiri")
	# 	# print(left.grid)
	# 	new_node = (current_path.get_path_length() + left.manhattan_distance_heuristic, current_path)
	# 	heappush(pq, new_node)

	if left not in visited_states:
		current_path = pq_node[1]
		# _heuristic_sum(state, down, "down", x,y)
		heuristic_value = _heuristic_sum_old(left)
		# print("kontol bawah")
		# print(down.grid)
		new_moves = list(moves)
		new_moves.append("LEFT")
		new_node = (length + heuristic_value, left, length + 1, new_moves)
		heappush(pq, new_node)



def calculate_manhattan_beginning(initial):
	n = len(initial)
	dist = 0
	for i in range(n):
		for j in range(n):
			number = initial[i][j]
			real_x_coordinate_of_number = (number-1) // n
			real_y_coordinate_of_number = (number-1) % n
			dist += distance(real_x_coordinate_of_number, real_y_coordinate_of_number, i, j)
	return dist