from CS3243_P1_37_1 import uninformed_search_test
from CS3243_P1_37_2 import informed_search_manhattan_test
from CS3243_P1_37_3 import informed_search_misplaced_tile_test
from CS3243_P1_37_4 import informed_search_linear_conflict_test
import time
import random
import math
from copy import deepcopy
 
def flatten(mat):
    tmp = []
    for row in mat:
        for x in row:
            tmp.append(x)
    return tmp
 
def pack(mat):
    size = int(math.sqrt(len(mat)))
    result = []
    for i in range(size):
        tmp = []
        for j in range(size):
            tmp.append(mat[i*size + j])
        result.append(tmp)
    return result

def create_test(n):
	num_of_tiles = n*n
	#random.seed(time.time())
	
	if n == 3:
		goal = [[1,2,3], [4,5,6], [7,8,0]]
	elif n == 4:
		goal = [[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,0]]
	elif n == 5:
		goal = [[1,2,3,4,5], [6,7,8,9,10], [11,12,13,14,15], [16,17,18,19,20], [21,22,23,24,0]]
	
	"""
	# Some mechanics to reduce the depth of the solution:
	# choose a random number of tiles to fix in their goal positions
	fixed_tiles = set()
	to_shuffle = []
	for i in range(num_of_tiles):
		if random.random() < .3: # fix about 30% of tiles
			fixed_tiles.add(i)
		else:
			to_shuffle.append(i)
	
	random.shuffle(to_shuffle)
	
	initial = []
	for i in range(num_of_tiles):
		j = (i+1)%num_of_tiles
		if j in fixed_tiles:
			initial.append(j)
		else:
			initial.append(to_shuffle.pop(0))
	
	# check number of inversions
	num_of_inversions = 0
	for i in range(num_of_tiles):
		if initial[i] == 0:
			continue
		for j in range(i):
			if initial[j] == 0:
				continue
			
			if initial[j] > initial[i]:
				num_of_inversions += 1
	
	print("Created test: " + str(initial) + ". Inversions: " + str(num_of_inversions))
	"""
	
	initial = deepcopy(goal)
	
	num_of_actions = 30 # guarantee to generate an initial state of depth at most this
	last_action = -1
	# coords of the empty tile
	x = n-1
	y = n-1
	for i in range(num_of_actions):
		while True:
			action = random.randint(0, 3)
			
			if action == last_action:
				continue
			
			if action == 0 and x > 0: # x-
				initial[x][y], initial[x-1][y] = initial[x-1][y], initial[x][y]
				x -= 1
				last_action = action
				break
			elif action == 1 and x < n-1: # x+
				initial[x][y], initial[x+1][y] = initial[x+1][y], initial[x][y]
				x += 1
				last_action = action
				break
			elif action == 2 and y > 0: # y-
				initial[x][y], initial[x][y-1] = initial[x][y-1], initial[x][y]
				y -= 1
				last_action = action
				break
			elif action == 3 and y < n-1: # y+
				initial[x][y], initial[x][y+1] = initial[x][y+1], initial[x][y]
				y += 1
				last_action = action
				break

	#print("Created test: " + str(initial))
	
	#initial = [i for i in range(num_of_tiles)]
	#random.shuffle(initial)
	#initial = pack(initial)
	return goal, initial


def performance():
	"""
	Evaluate the performance of informed & uninformed search algorithms.
	
	Metrics:
	- time taken to run the search
	- length of the optimal path found
	"""
	# get test parameters
	print("Please enter the size from 3 to 5:")
	grid_size = int(input())
	print("Please enter the number of tests you want to run:")
	num_of_tests = int(input())
	
	# get aggregate scores per depth
	depths = [{},{},{},{}] # depths[algo_index][depth] = (total_num_of_tests, total_time_taken, total_nodes_seen)
	tests_left = num_of_tests

	test_names = ["A* with Linear Conflict Heuristic", "A* with Manhattan Distance Heuristic", "A* with Misplaced Tile Heuristic", "BFS Uninformed"]
	
	print("Running " + str(tests_left) + " tests...")
	while tests_left > 0:
		test_index = num_of_tests - tests_left + 1
		goal, initial = create_test(grid_size)
		path_length = -1
		
		for algo_index in range(4):
			# Do NOT ask BFS to solve initial states with depth past a certain point or for anything more than 3x3 puzzles, the time and space needed is unfeasible
			if algo_index == 3 and (grid_size > 3 or path_length > 20):
				continue
			
			time_taken, nodes_seen, path_length = timer(initial, goal, test_names[algo_index] + " " + str(test_index), algo_index)
			
			if path_length < 0: # got an unsolvable problem
				break # break out of for loop
			
			if path_length in depths[algo_index]:
				depths[algo_index][path_length][0] += 1
				depths[algo_index][path_length][1] += time_taken
				depths[algo_index][path_length][2] += nodes_seen
			else:
				depths[algo_index][path_length] = [1, time_taken, nodes_seen]
		
		if path_length >= 0:
			if test_index%10 == 0:
				print("Test " + str(test_index) + " done. Depth: " + str(path_length))
			tests_left -= 1
	
	# print results
	print("Tests done!")
	for algo_index in range(4):
		print("\nResults for " + test_names[algo_index] + ":")
		
		for depth in depths[algo_index]:
			print("Depth: " + str(depth))
			
			total_num_of_tests = depths[algo_index][depth][0]
			avg_time_taken = depths[algo_index][depth][1] / total_num_of_tests
			avg_nodes_seen = depths[algo_index][depth][2] / total_num_of_tests
			
			print("    Total num of tests: " + str(total_num_of_tests))
			print("    Average time: " + str(avg_time_taken) + " ms")
			print("    Average nodes seen: " + str(avg_nodes_seen))


def timer(test, goal, testname, mode):
	#print("Running: " + testname)
	
	# record elapsed time
	start = time.time()
	
	# This is NOT in the order of the source code files
	# Instead it is ordered from fastest first
	if mode == 0:
		run = informed_search_linear_conflict_test(test, goal)
	elif mode == 1:
		run = informed_search_manhattan_test(test, goal)
	elif mode == 2:
		run = informed_search_misplaced_tile_test(test, goal)
	elif mode == 3:
		run = uninformed_search_test(test, goal)
	
	end = time.time()
	time_taken = (end - start)*1000 # in ms
	#print(testname + ": %.8f ms" %time_taken)
	
	nodes_seen = run[1]
	path = run[0]
	# record optimal path length found
	path_length = len(path)
	if (isinstance(path, list) and path_length == 1 and path[0] == "UNSOLVABLE"):
		path_length = -1 # indicate an unsolvable state with a path length of -1
		#print("Path length: UNSOLVABLE")
	#else:
		#print("Path length: " + str(path_length))
	
	#print("Nodes seen: " + str(nodes_seen))
	
	return (time_taken, nodes_seen, path_length)
 
 
 
if __name__ == '__main__':
    performance()