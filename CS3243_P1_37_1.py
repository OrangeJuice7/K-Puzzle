import os
import sys


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()

    def solve(self):
        return self.uninformed_search(init_state, goal_state)

    # you may add more functions if you think is useful
    def uninformed_search(self, initial, goal):
        # both inputs are 2D arrays with integer value in each cell.
        
        # record all the moves to achieve the goal in an ordered list
        moves = []

        # mark the visited states in the BFS
        visited = set()

        # check whether the puzzle has a valid solution
        if self.isSolvable(initial):
            # run the BFS
            # it returns the list of moves that constitutes the path to goal
            path_merged = self.bfs(initial, goal, visited)
            path = path_merged[0]
            path.pop(0) # remove start node

            # each move is a tuple (next_state, next_move)
            for move in path:
                moves.append(move[1])
        else:
            # the puzzle cannot be solved
            moves.append("UNSOLVABLE")
            
        return moves

    # you may add more functions if you think is useful
    def uninformed_search_test(self, initial, goal):
        # both inputs are 2D arrays with integer value in each cell.
        
        # record all the moves to achieve the goal in an ordered list
        moves = []

        # mark the visited states in the BFS
        visited = set()

        # check whether the puzzle has a valid solution
        if self.isSolvable(initial):
            # run the BFS
            # it returns the list of moves that constitutes the path to goal
            path_merged = self.bfs(initial, goal, visited)
            path = path_merged[0]
            path.pop(0) # remove start node

            # each move is a tuple (next_state, next_move)
            for move in path:
                moves.append(move[1])

            moves = [moves, path_merged[1]]
        else:
            # the puzzle cannot be solved
            moves.append("UNSOLVABLE")
            moves = [moves, 1]
            
        return moves
        
    def bfs(self, initial, goal, visited):
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
        node_seen = 0
        while (len(queue) != 0):
            path = queue.pop(0)
            state = path[-1][0]
            node_seen += 1
            # check terminating condition
            if self.isreached(state, goal):
                node_seen += len(queue)
                return [path, node_seen]

            # find the coordinate of the blank cell
            x, y = self.locateblank(state)

            if 0 <= (x-1) < len(state):
                down = self.swap(state, x-1, y, x, y)
                if down not in visited:
                    npath = list(path)
                    move = (down, "DOWN")
                    # update the path to explore the next neighbour state
                    npath.append(move)
                    queue.append(npath)

            if 0 <= (y-1) < len(state[0]):
                right = self.swap(state, x, y-1, x, y)
                if right not in visited:
                    npath = list(path)
                    move = (right, "RIGHT")
                    # update the path to explore the next neighbour state
                    npath.append(move)
                    queue.append(npath)

            if (x+1) < len(state):
                up = self.swap(state, x+1, y, x, y)
                if up not in visited:
                    npath = list(path)
                    move = (up, "UP")
                    # update the path to explore the next neighbour state
                    npath.append(move)
                    queue.append(npath)

            if (y+1) < len(state[0]):
                left = self.swap(state, x, y+1, x, y)
                if left not in visited:
                    npath = list(path)
                    move = (left, "LEFT")
                    # update the path to explore the next neighbour state
                    npath.append(move)
                    queue.append(npath)

            # mark the current state as visited
            visit = tuple(map(tuple, state))
            visited.add(visit)
        
            
    def swap(self, state, nx, ny, ox, oy):
        # swap the values of two cells in the puzzle
        transform = list(map(list, state))

        temp = transform[ox][oy]
        transform[ox][oy] = transform[nx][ny]
        transform[nx][ny] = temp
        
        res = tuple(map(tuple, transform))

        return res


    def locateblank(self, state):
        # find the coordinates of the blank cell (0)
        # in the puzzle grid
        for i in range(0, len(state)):
            for j in range(0, len(state[0])):
                if state[i][j] == 0:
                    return i, j

        raise ValueError("Error: no blank cell exists!")


    def isreached(self, state, goal):
        # check whether the current state is equal
        # to the goal state
        state = list(map(list, state))
        for i in range(0, len(state)):
            for j in range(0, len(state[0])):
                if (state[i][j] != goal[i][j]): 
                    return False

        return True


    def isSolvable(self, state):
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

def uninformed_search_test(initial, goal):
    puzzle = Puzzle(initial, goal)
    return puzzle.uninformed_search_test(initial, goal)

if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()
    
    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]
    

    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')