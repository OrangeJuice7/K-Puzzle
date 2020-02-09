from heapq import heappush
from heapq import heappop


def informed(initial, goal):
	# both inputs are 2D arrays with integer value in each cell.
    
    # record all the moves to achieve the goal in an ordered list
    moves = []

    # mark the visited states in the A* search
    visited = set()

    # check whether the puzzle has a valid solution
    if isSolvable(initial):
    	# run the A* search algorithm
    	# it returns tuple (sort_key, path)
        path = astar(initial, goal, visited)
        path = path[1]
        path.pop(0) # remove start node

        # the path constitutes a list of moves to goal
        # each move is a tuple (next_state, next_move)
        for move in path:
            moves.append(move[1])
    else:
    	# the puzzle cannot be solved
    	moves.append("UNSOLVABLE")
        
    return moves


def astar(initial, goal, visited):
	"""
	We maintain a priority queue that sort the path based on 
	heuristics. And explore the next state with lowest expected cost.

	Each entry of the priority queue is a tuple (heuristic_sort_key, path)
	Each path is a list of tuples (next 2D state, the move to achieve next state)
	
	By default, Python priority queue sort the tuple based on the first 
	element of that tuple.

	Evaluation function 
		= current length of the path + Manhattan distance of each tile from its proper position
	
    When the goal state is reached, we return the path from source to goal.
	"""
	start = (initial, "-")
	source = (0, [start])

	pq = [] # use the priority queue
	heappush(pq, source)

	while (len(pq) != 0):
		# retrieve the path with lowest expected cost
		path = heappop(pq)
		state = path[1][-1][0]
    	# check terminating condition
		if isreached(state, goal):
			return path

        # find the coordinate of the blank cell
		x, y = locateblank(state)

		if 0 <= (x-1) < len(state):
			down = swap(state, x-1, y, x, y)
			if down not in visited:
				npath = path[1].copy()
				move = (down, "DOWN")
				# update the path to explore the next neighbour state
				npath.append(move)
				# calculate the heuristic and form the tuple entry
				# for ranking in priority queue
				apath = (len(npath) + heuristic_sum(down), npath)
				heappush(pq, apath)

		if 0 <= (y-1) < len(state[0]):
			right = swap(state, x, y-1, x, y)
			if right not in visited:
				npath = path[1].copy()
				move = (right, "RIGHT")
				# update the path to explore the next neighbour state
				npath.append(move)
				# calculate the heuristic and form the tuple entry
				# for ranking in priority queue
				apath = (len(npath) + heuristic_sum(right), npath)
				heappush(pq, apath)

		if (x+1) < len(state):
			up = swap(state, x+1, y, x, y)
			if up not in visited:
				npath = path[1].copy()
				move = (up, "UP")
				# update the path to explore the next neighbour state
				npath.append(move)
				# calculate the heuristic and form the tuple entry
				# for ranking in priority queue
				apath = (len(npath) + heuristic_sum(up), npath)
				heappush(pq, apath)

		if (y+1) < len(state[0]):
			left = swap(state, x, y+1, x, y)
			if left not in visited:
				npath = path[1].copy()
				move = (left, "LEFT")
				# update the path to explore the next neighbour state
				npath.append(move)
				# calculate the heuristic and form the tuple entry
				# for ranking in priority queue
				apath = (len(npath) + heuristic_sum(left), npath)
				heappush(pq, apath)

        # mark the current state as visited
		visit = tuple(map(tuple, state))
		visited.add(visit)


def heuristic_sum(state):
	# the total distance between every misplaced tile and its expected position
	n = len(state)
	total = 0

	for i in range(0, n):
		for j in range(0, n):
			num = state[i][j]
			if num == 0:
				continue
			# offset = current pos - expected pos
			disx = abs(i - (num - 1) // n)
			disy = abs(j - (num - 1) % n)
			total = total + disx + disy

	return total


def swap(state, nx, ny, ox, oy):
	# swap the values of two cells in the puzzle
	transform = list(map(list, state))

	temp = transform[ox][oy]
	transform[ox][oy] = transform[nx][ny]
	transform[nx][ny] = temp
    
	res = tuple(map(tuple, transform))

	return res


def locateblank(state):
	# find the coordinates of the blank cell (0)
	# in the puzzle grid
	for i in range(0, len(state)):
		for j in range(0, len(state[0])):
			if state[i][j] == 0:
				return i, j

	raise ValueError("Error: no blank cell exists!")


def isreached(state, goal):
	# check whether the current state is equal
	# to the goal state
	state = list(map(list, state))
	for i in range(0, len(state)):
		for j in range(0, len(state[0])):
			if (state[i][j] != goal[i][j]): 
				return False

	return True


def isSolvable(state):
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

