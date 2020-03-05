import os
import sys
from heapq import heappush
from heapq import heappop


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()

    def solve(self):        
        self.actions = self.informed_search_misplaced_tile(self.init_state, self.goal_state)
        return self.actions

    # you may add more functions if you think is useful
    '''
    informed_search is a method that defines the general procedure
    of doing an informed search from the state to the goal. The function
    takes in an initial state, as well as the goal state. A state is represented
    as a 2D array. The function returns the
    sequence of moves to solve the puzzle. It will return unsolvable.
    '''

    def informed_search_misplaced_tile(self, initial, goal):
        moves = self._initialize_list()
        visited_states = {}
        initial = tuple(map(tuple, initial))
        if self._is_solvable(initial):
            path = self._run_astar(initial, goal, visited_states, moves)
            return path[3]
            
        else:
            self._mark_unsolvable(moves)
            
        return moves

    def informed_search_misplaced_tile_test(self, initial, goal):
        moves = self._initialize_list()
        visited_states = {}
        initial = tuple(map(tuple, initial))
        if self._is_solvable(initial):
            path = self._run_astar(initial, goal, visited_states, moves)
            return [path[3], path[4]]
            
        else:
            self._mark_unsolvable(moves)
            
        return [moves, 1]

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

    def _run_astar(self, initial, goal, visited_states, moves):
        source = (0, initial, 0, moves)
        pq = []
        heappush(pq, source)
        node_seen = 0
        while (len(pq) != 0):
            pq_node = heappop(pq)
            state = pq_node[1]
            node_seen += 1
            if self._is_reached(state, goal):
                node_seen += len(pq)
                pq_node = list(pq_node)
                pq_node.append(node_seen)
                return pq_node

            if visited_states[state] == 1:
                continue

            x, y = self._locate_blank(state)

            if self._is_moved_down(x, state):
                self._move_down(state, x, y, visited_states, pq, pq_node, pq_node[2], pq_node[3])

            if self._is_moved_right(y, state):
                self._move_right(state, x, y, visited_states, pq, pq_node, pq_node[2], pq_node[3])

            if self._is_moved_up(x, state):
                self._move_up(state, x, y, visited_states, pq, pq_node, pq_node[2], pq_node[3])

            if self._is_moved_left(y, state):
                self._move_left(state, x, y, visited_states, pq, pq_node, pq_node[2], pq_node[3])

            visited_states[state] = 1


    def _swap(self, state, nx, ny, ox, oy):
        transform = list(map(list, state))
        temp = transform[ox][oy]
        transform[ox][oy] = transform[nx][ny]
        transform[nx][ny] = temp
        
        res = tuple(map(tuple, transform))
        return res


    def _locate_blank(self, state):
        for i in range(0, len(state)):
            for j in range(0, len(state[0])):
                if state[i][j] == 0:
                    return i, j

        raise ValueError("Error: no blank cell exists!")


    def _is_reached(self,state, goal):
        for i in range(0, len(state)):
            for j in range(0, len(state[0])):
                if (state[i][j] != goal[i][j]): 
                    return False

        return True


    def _is_solvable(self, state):
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

    def _heuristic_sum(self, current_state):
        return self.calculate_misplaced_distance(current_state)

    '''
    _mark_unsolvable is an internal method to mark that the puzzle is not
    unsolvable. It takes in a sequence of moves in form of list, and append
    the unsolvable mark to the list.
    '''

    def _mark_unsolvable(self, moves):
        moves.append("UNSOLVABLE")

    '''
    _initialize_list is an internal method to abstract the list creation.
    '''

    def _initialize_list(self):
        return []

    '''
    _remove_sort_key is an internal method to remove the sort_key after doing
    the A* search. It takes in the result of A* search, and returns the path
    to reach the goal state. The result of A* search is in form of (sort_key, path).
    '''

    def _remove_sort_key(self, path):
        return path[1]

    '''
    _remove_start_node is an internal method to remove the start node.
    '''

    def _remove_start_node(self, path):
        return path.remove_first()

    '''
    _add_moves adds all the moves from the A* search to the original list.
    Each move is in form (next_state, next_move)
    '''

    def _add_moves(self, moves, path):
        for move in path.moves:
            moves.append(move.direction)

    '''
    _is_moved_down checks whether there exists a tile that can be moved down.
    '''

    def _is_moved_down(self, x, state):
        return 0 <= (x-1) < len(state)

    '''
    _is_moved_up checks whether there exists a tile that can be moved up.
    '''

    def _is_moved_up(self, x, state):
        return 0 <= (x+1) < len(state)

    '''
    _is_moved_left checks whether there exists a tile that can be moved left.
    '''

    def _is_moved_left(self, y, state):
        return (y+1) < len(state[0])
    '''
    _is_moved_right checks whether there exists a tile that can be moved right.
    '''

    def _is_moved_right(self, y, state):
        return 0 <= (y-1) < len(state[0])

    '''
    _move_down moves the tile down to the blank tile.
    '''

    def distance(self, x1, y1, x2, y2):
        return abs(x1-x2) + abs(y1 - y2)

    def _move_down(self, state, x, y, visited_states, pq, pq_node, length, moves):
        down = self._swap(state, x-1, y, x, y)

        if down not in visited_states:
            current_path = pq_node[1]
            heuristic_value = self._heuristic_sum(down)
            new_moves = list(moves)
            new_moves.append("DOWN")
            new_node = (length + heuristic_value, down, length + 1, new_moves)
            heappush(pq, new_node)

    '''
    _move_up moves the tile up to the blank tile.
    '''

    def _move_up(self, state, x, y, visited_states, pq, pq_node, length, moves):
        up = self._swap(state, x+1, y, x, y)

        if up not in visited_states:
            current_path = pq_node[1]
            heuristic_value = self._heuristic_sum(up)
            new_moves = list(moves)
            new_moves.append("UP")
            new_node = (length + heuristic_value, up, length + 1, new_moves)
            heappush(pq, new_node)


    '''
    _move_right moves the tile right to the blank tile.
    '''

    def _move_right(self, state, x, y, visited_states, pq, pq_node, length, moves):
        right = self._swap(state, x, y-1, x, y)

        if right not in visited_states:
            current_path = pq_node[1]
            heuristic_value = self._heuristic_sum(right)
            new_moves = list(moves)
            new_moves.append("RIGHT")
            new_node = (length + heuristic_value, right, length + 1, new_moves)
            heappush(pq, new_node)


    '''
    _move_left moves the tile left to the blank tile.
    '''

    def _move_left(self, state, x, y, visited_states, pq, pq_node, length, moves):
        left = self._swap(state, x, y+1, x, y)

        if left not in visited_states:
            current_path = pq_node[1]
            heuristic_value = self._heuristic_sum(left)

            new_moves = list(moves)
            new_moves.append("LEFT")
            new_node = (length + heuristic_value, left, length + 1, new_moves)
            heappush(pq, new_node)

    def calculate_misplaced_distance(self, initial):
        n = len(initial)
        total = 0
        for i in range(n):
            for j in range(n):
                number = initial[i][j]
                if (number - 1) // n != i or (number - 1) % n != j:
                    total += 1;
        return total

def informed_search_misplaced_tile_test(initial, goal):
    puzzle = Puzzle(initial, goal)
    return puzzle.informed_search_misplaced_tile_test(initial, goal)


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