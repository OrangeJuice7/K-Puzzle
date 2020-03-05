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
    print("Please enter the size from 3 to 5:")
    n = int(input())
    print("Please enter the number of tests you want to run:")
    t = int(input())
    print("Please enter the mode you want to use:\n1. BFS Uninformed\n2. A* with Manhattan Distance Heuristic\n3. A* with Misplaced Tile Heuristic\n4. A* with Linear Conflict Heuristic")
    h = int(input())
    times = []
    test_names = ["BFS Uninformed", "A* with Manhattan Distance Heuristic", "A* with Linear Conflict Heuristic", "A* with Misplaced Tile Heuristic"]
    for i in range(t):
        goal, initial = create_test(n)
        times.append(timer(initial, goal, test_names[h - 1] + " " + str(i+1), h))
    print("Average time: " + str(sum(times)/len(times)))
 
 
def timer(test, goal, testname, mode):
    # record elapsed time
    start = time.time()
    if mode == 1:
        run = uninformed_search_test(test, goal)
    elif mode == 2:
        run = informed_search_manhattan_test(test, goal)
    elif mode == 3:
        run = informed_search_misplaced_tile_test(test, goal)
    elif mode == 4:
        run = informed_search_linear_conflict_test(test, goal)
    end = time.time()
    print(testname + ": %.8f s" %(end - start))
    node_seen = run[1]
    run = run[0]
    # record optimal path length found
    if (isinstance(run, list) and len(run) == 1 and run[0] == "UNSOLVABLE"):
        print("path length: UNSOLVABLE")
    else:
        print("path length: " + str(len(run)))
    print("Node seen: " + str(node_seen))
 
    return end - start
 
 
 
if __name__ == '__main__':
    performance()