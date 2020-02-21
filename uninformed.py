def uninformed_search(initial, goal):
	# both inputs are 2D arrays with integer value in each cell.
    
    # record all the moves to achieve the goal in an ordered list
    moves = []

    # mark the visited states in the BFS
    visited = set()

    # check whether the puzzle has a valid solution
    if isSolvable(initial):
    	# run the BFS
    	# it returns the list of moves that constitutes the path to goal
        path = bfs(initial, goal, visited)
        path.pop(0) # remove start node

        # each move is a tuple (next_state, next_move)
        for move in path:
            moves.append(move[1])
    else:
    	# the puzzle cannot be solved
    	moves.append("UNSOLVABLE")
        
    return moves

    
def bfs(initial, goal, visited):
	"""
    We maintain a queue to explore the neighbouring moves in a breath-first
    approach.

    Each entry in the queue is a valid path, which consists of a list of moves
    we have explored so far.
    Each move is a tuple (next_state, next_move)

    When the goal state is reached, we return the path from source to goal.
	"""
	start = (initial, "-")
	source = [start]

	queue = []
	queue.append(source)

	while (len(queue) != 0):
		path = queue.pop(0)
		state = path[-1][0]
    	# check terminating condition
		if isreached(state, goal):
			return path

        # find the coordinate of the blank cell
		x, y = locateblank(state)

		if 0 <= (x-1) < len(state):
			down = swap(state, x-1, y, x, y)
			if down not in visited:
				npath = path.copy()
				move = (down, "DOWN")
				# update the path to explore the next neighbour state
				npath.append(move)
				queue.append(npath)

		if 0 <= (y-1) < len(state[0]):
			right = swap(state, x, y-1, x, y)
			if right not in visited:
				npath = path.copy()
				move = (right, "RIGHT")
				# update the path to explore the next neighbour state
				npath.append(move)
				queue.append(npath)

		if (x+1) < len(state):
			up = swap(state, x+1, y, x, y)
			if up not in visited:
				npath = path.copy()
				move = (up, "UP")
				# update the path to explore the next neighbour state
				npath.append(move)
				queue.append(npath)

		if (y+1) < len(state[0]):
			left = swap(state, x, y+1, x, y)
			if left not in visited:
				npath = path.copy()
				move = (left, "LEFT")
				# update the path to explore the next neighbour state
				npath.append(move)
				queue.append(npath)

        # mark the current state as visited
		visit = tuple(map(tuple, state))
		visited.add(visit)
    
    	
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

