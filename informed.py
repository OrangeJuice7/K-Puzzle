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
    visited_state = set()

    if _is_solvable(initial):
    	initial_state = State(initial, True, 0)
        path = _run_astar(initial, goal, visited_states)
        path = _remove_sort_key(path)
        _remove_start_node(path)
        
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

def _run_astar(initial, goal, visited_states):

	start = _create_move(initial, "-")
	source = (0, Path(start))

	pq = []
	heappush(pq, source)

	while (len(pq) != 0):
		pq_node = heappop(pq)
		state = _get_most_recent_state(pq_node[1])

		if _is_reached(state.grid, goal):
			return pq_node

		x, y = _locate_blank(state)

		if _is_moved_down(x, state):
			_move_down(state, x, y, visited_states, pq)

		if _is_moved_right(y, state):
			_move_right(state, x, y, visited_states, pq)

		if _is_moved_up(x, state):
			_move_up(state, x, y, visited_states, pq)

		if _is_moved_left(y, state):
			_move_left(state, x, y, visited_states, pq)

        # mark the current state as visited
		visit = tuple(map(tuple, state.grid))
		visited.add(visit)


def _heuristic_sum(previous_state, current_state):
	# # the total distance between every misplaced tile and its expected position
	# n = len(state)
	# total = 0

	# for i in range(0, n):
	# 	for j in range(0, n):
	# 		num = state[i][j]
	# 		if num == 0:
	# 			continue
	# 		# offset = current pos - expected pos
	# 		disx = abs(i - (num - 1) // n)
	# 		disy = abs(j - (num - 1) % n)
	# 		total = total + disx + disy

	# Fill in as desired!

	return total


def _swap(state, nx, ny, ox, oy):
	transform = list(map(list, state.grid))

	temp = transform[ox][oy]
	transform[ox][oy] = transform[nx][ny]
	transform[nx][ny] = temp
    
	res = tuple(map(tuple, transform))

	return State(res, False, state.manhattan_distance_heuristic)


def _locate_blank(state):
	# find the coordinates of the blank cell (0)
	# in the puzzle grid
	for i in range(0, len(state)):
		for j in range(0, len(state[0])):
			if state[i][j] == 0:
				return i, j

	raise ValueError("Error: no blank cell exists!")


def _is_reached(state, goal):
	# check whether the current state is equal
	# to the goal state
	state = list(map(list, state))
	for i in range(0, len(state)):
		for j in range(0, len(state[0])):
			if (state[i][j] != goal[i][j]): 
				return False

	return True


def _is_solvable(state):
	# the puzzle is solvable if there are even number
	# of inversion pairs; otherwise, it is not solvable
    inv_count = 0

    # flattent the array from 2D into 1D
    flat = []
    for i in range(0, len(state)):
    	for j in range(0, len(state[0])):
    		flat.append(state[i][j])

    # count inversion pairs
    for m in range(0, len(flat)-1):
    	for n in range(m, len(flat)):
    		if (flat[m] and flat[n] and flat[m] > flat[n]):
    			inv_count += 1

    return inv_count % 2 == 0

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
	path.pop(0)

'''
_add_moves adds all the moves from the A* search to the original list.
Each move is in form (next_state, next_move)
'''

def _add_moves(moves, path):
	for move in path:
    	moves.append(move[1])

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
	return 0 <= (x-1) < state.get_grid_size()

'''
_is_moved_up checks whether there exists a tile that can be moved up.
'''

def _is_moved_up(x, state):
	return (x+1) < state.get_grid_size()

'''
_is_moved_left checks whether there exists a tile that can be moved left.
'''

def _is_moved_left(y, state):
	return (y+1) < state.get_grid_size()

'''
_is_moved_right checks whether there exists a tile that can be moved right.
'''

def _is_moved_right(y, state):
	return 0 <= (y-1) < state.get_grid_size()

'''
_move_down moves the tile down to the blank tile.
'''

def _move_down(state, x, y, visited_states, pq):
	down = _swap(state, x-1, y, x, y)
	if down.grid not in visited_states:
		current_path = pq_node[1]
		heuristic_value = heuristic_sum(state, down)
		down.manhattan_distance_heuristic = heuristic_value
		current_path.add_move(Move(down, "DOWN"))
		new_node = (current_path.get_path_length() + heuristic_value, current_path)
		heappush(pq, new_node)

'''
_move_up moves the tile up to the blank tile.
'''

def _move_up(state, x, y, visited_states, pq):
	up = _swap(state, x+1, y, x, y)
	if up.grid not in visited_states:
		current_path = pq_node[1]
		heuristic_value = heuristic_sum(state, up)
		up.manhattan_distance_heuristic = heuristic_value
		current_path.add_move(Move(up, "UP"))
		new_node = (current_path.get_path_length() + heuristic_value, current_path)
		heappush(pq, new_node)

'''
_move_right moves the tile right to the blank tile.
'''

def _move_right(state, x, y, visited_states, pq):
	right = _swap(state, x, y-1, x, y)
	if right.grid not in visited_states:
		current_path = pq_node[1]
		heuristic_value = heuristic_sum(state, right)
		right.manhattan_distance_heuristic = heuristic_value
		current_path.add_move(Move(right, "RIGHT"))
		new_node = (current_path.get_path_length() + heuristic_value, current_path)
		heappush(pq, new_node)

'''
_move_left moves the tile left to the blank tile.
'''

def _move_left(state, x, y, visited_states, pq):
	left = _swap(state, x, y+1, x, y)
	if left.grid not in visited_states:
		current_path = pq_node[1]
		heuristic_value = heuristic_sum(state, left)
		left.manhattan_distance_heuristic = heuristic_value
		current_path.add_move(Move(left, "LEFT"))
		new_node = (current_path.get_path_length() + heuristic_value, current_path)
		heappush(pq, new_node)