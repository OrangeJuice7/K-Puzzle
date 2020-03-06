from CS3243_P1_37_1 import uninformed_search_test
from CS3243_P1_37_2 import informed_search_manhattan_test
from CS3243_P1_37_3 import informed_search_misplaced_tile_test
from CS3243_P1_37_4 import informed_search_linear_conflict_test
import time
import random
import math
 
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
    if n == 3:
        goal = [[1,2,3], [4,5,6], [7,8,0]]
    elif n == 4:
        goal = [[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,0]]
    elif n == 5:
        goal = [[1,2,3,4,5], [6,7,8,9,10], [11,12,13,14,15], [16,17,18,19,20], [21,22,23,24,0]]
 
    initial = goal
    initial = flatten(initial)
    random.shuffle(initial)
    initial = pack(initial)
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
		goal, initial = create_test(grid_size)
		path_length = -1
		
		for algo_index in range(4):
			time_taken, nodes_seen, path_length = timer(initial, goal, test_names[algo_index] + " " + str(tests_left), algo_index)
			
			if path_length < 0: # got an unsolvable problem
				break # break out of for loop
			
			if path_length in depths[algo_index]:
				depths[algo_index][path_length][0] += 1
				depths[algo_index][path_length][1] += time_taken
				depths[algo_index][path_length][2] += nodes_seen
			else:
				depths[algo_index][path_length] = [1, time_taken, nodes_seen]
		
		if path_length >= 0:
			tests_left -= 1
			print("Depth: " + str(path_length) + "    Tests left: " + str(tests_left))
	
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
			print("    Average time: " + str(avg_time_taken))
			print("    Average nodes seen: " + str(avg_nodes_seen))


def timer(test, goal, testname, mode):
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
	time_taken = end - start
	#print(testname + ": %.8f s" %time_taken)
	
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