from informed3 import informed_search
from uninformed import uninformed_search
import time


def performace():
	"""
    Evaluate the performance of informed & uninformed search algorithms.
    
    Metrics:
    - time taken to run the search
    - length of the optimal path found
	"""

	# Test input for 3*3 puzzle
	test_3_1 = [[1,2,3], [4,5,6], [8,7,0]]
	test_3_2 = [[1,8,3], [5,2,4], [0,7,6]]
	test_3_3 = [[8,6,7], [2,5,4], [3,0,1]]
    # Test input for 4*4 puzzle
	test_4_1 = [[1,2,3,4], [5,6,7,8], [10,11,0,12], [9,13,15,14]]
	test_4_2 = [[12,15,6,10], [4,9,5,8], [14,13,0,2], [1,7,11,3]]
	# test_4_3 = [[14,10,5,13], [11, 8, 1, 3], [2,9,12,6], [15,4,0,7]]
	test_4_3 = [[13, 5, 3, 4], [2, 1, 8, 0], [9, 15, 10, 11], [14, 12, 6, 7]]
	test_4_4 = [[9, 5, 12, 4], [0, 1, 3, 10], [14, 13, 11, 2], [15, 7, 6, 8]]
	# Test input for 5*5 puzzle
	# test_5_1 = [[1,2,3,4,5], [6,7,8,9,10], [11,12,0,14,15], [16,17,13,18,19], [21,22,23,20,24]]
	# test_5_2 = [[5,7,20,18,8], [14,16,4,23,3], [1,11,2,24,13], [21,10,19,0,17], [15,12,6,22,9]]
	# test_5_3 = [[21,12,8,18,20], [24,1,17,13,11], [22,4,19,9,5], [15,2,10,0,16], [7,23,6,14,3]]
	test_5_1 = [[1,2,3,4,5], [6,7,8,9,10], [11,12,0,14,15], [16,17,13,20,19], [21,22,23,18,24]]
	test_5_2 = [[1, 3, 4, 10, 5], [7, 2, 8, 0, 14], [6, 11, 12, 9, 15], [16, 17, 13, 18, 19], [21, 22, 23, 24, 20]]
	test_5_3 = [[1, 3, 4, 0, 10], [7, 2, 12, 8, 5], [6, 11, 13, 15, 14], [17, 23, 18, 9, 19], [16, 21, 22, 24, 20]]
	test_5_4 = [[1, 3, 4, 10, 5], [7, 2, 12, 8, 14], [6, 11, 13, 15, 0], [17, 23, 18, 9, 19], [16, 21, 22, 24, 20]]
	test_5_5 = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 14, 0, 15], [16, 17, 13, 18, 19], [21, 22, 23, 24, 20]]


    # Goal states
	goal_3 = [[1,2,3], [4,5,6], [7,8,0]]
	goal_4 = [[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,0]]
	goal_5 = [[1,2,3,4,5], [6,7,8,9,10], [11,12,13,14,15], [16,17,18,19,20], [21,22,23,24,0]]

	# Test for uninformed search
	# timer(test_3_1, goal_3, "test_3_1", False)
	# timer(test_3_2, goal_3, "test_3_2", False)
	# timer(test_3_3, goal_3, "test_3_3", False)

	# timer(test_4_1, goal_4, "test_4_1", False)
	# timer(test_4_2, goal_4, "test_4_2", False)
	# timer(test_4_3, goal_4, "test_4_3", False)

	#timer(test_5_1, goal_5, "test_5_1", False)
	#timer(test_5_2, goal_5, "test_5_2", False)
	#timer(test_5_3, goal_5, "test_5_3", False)

	# Test for informed search
	# timer(test_3_1, goal_3, "test_3_1", True)
	# timer(test_3_2, goal_3, "test_3_2", True)
	# timer(test_3_3, goal_3, "test_3_3", True)

	timer(test_4_1, goal_4, "test_4_1", True)
	timer(test_4_2, goal_4, "test_4_2", True)
	timer(test_4_3, goal_4, "test_4_3", True)
	timer(test_4_4, goal_4, "test_4_4", True)

	# timer(test_5_1, goal_5, "test_5_1", True)
	# timer(test_5_2, goal_5, "test_5_2", True)
	# timer(test_5_3, goal_5, "test_5_3", True)
	# timer(test_5_4, goal_5, "test_5_4", True)	
	# timer(test_5_5, goal_5, "test_5_5", True)

def timer(test, goal, testname, is_informed):
	# record elapsed time
	start = time.time()
	if (not is_informed):
		run = uninformed_search(test, goal)
	else:
		run = informed_search(test, goal)
	end = time.time()
	print(testname + ": %.8f s" %(end - start))

	# record optimal path length found
	if (isinstance(run, list) and len(run) == 1 and run[0] == "UNSOLVABLE"):
		print("path length: UNSOLVABLE")
	else:
		print("path length: " + str(len(run)))



if __name__ == '__main__':
	performace()
