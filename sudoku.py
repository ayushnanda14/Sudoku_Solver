from time import process_time
from copy import deepcopy
import json

def printMatrix(lis):
    strn = "\n" + 7*"\t"
    
    for i in range(len(lis)):
        ch = " "
        if i % 9 == 8:
            ch = "\n" + 7*"\t"
        strn += str(lis[i]) + ch
        # print(lis[i], end=ch)
    # print(strn)
    return strn
    

from search import *

class SudokuProblem(Problem):
    def __init__(self, initial):
        super().__init__(initial)
        self.dic1 = {}
        self.dic2 = {}
        self.dic2[0] = [0, 1, 2, 9, 10, 11, 18, 19, 20]
        self.dic2[1] = [3, 4, 5, 12, 13, 14, 21, 22, 23]
        self.dic2[2] = [6, 7, 8, 15, 16, 17, 24, 25, 26]
        self.dic2[3] = [27, 28, 29, 36, 37, 38, 45, 46, 47]
        self.dic2[4] = [30, 31, 32, 39, 40, 41, 48, 49, 50]
        self.dic2[5] = [33, 34, 35, 42, 43, 44, 51, 52, 53]
        self.dic2[6] = [54 ,55 ,56, 63 ,64 ,65, 72 ,73 ,74]
        self.dic2[7] = [57, 58, 59, 66, 67, 68, 75, 76, 77]
        self.dic2[8] = [60, 61, 62, 69, 70, 71, 78, 79, 80]

        for i in self.dic2:
            for j in self.dic2[i]:
                self.dic1[j] = i
        
        

    #Finds the next Unfilled Cell in the State    
    def find_unfilled_cell(self, state):
        try:
            ans = state.index(0)
        except(ValueError):
            ans = -1
        
        return ans
    
    #Checks if the current state satisfies the Sudoku Rule
    def isSafe(self, state , ind, k):
        i = -9
        #Check Up
        while(ind + i > -1):
            if state[ind + i] == k:
                return False
            i -= 9
        
        i = 9
        #Check Down
        while(ind + i < 81):
            if state[ind + i] == k:
                return False
            i += 9 

        #Check right
        for i in range(1,9 - ind%9):
            if state[ind + i] == k:
                return False

        #Check left
        for i in range(-1,ind%9 * -1 -1, -1):
            if state[ind + i] == k:
                return False

        #Check 3x3
        block = self.dic1[ind]
        # print(self.dic2[block], ind)
        # self.dic2[block].remove(ind)
        for i in self.dic2[block]:
            # print(i,end=" ")
            if i==ind:
                continue
            if state[i] == k:
                return False
        # self.dic2[block].append(ind)
        
        # print()
        return True
    
    def makeList(self, state, ind):
        ls = []
        for k in range(1,10):
            if self.isSafe(state, ind ,k):
                ls.append(k)
        return ls


    def actions(self, state):
        unfc = self.find_unfilled_cell(state)
        return self.makeList(state, unfc)

    def result(self, state, action):
        unfc = self.find_unfilled_cell(state)
        next_state = deepcopy(state)
        next_state[unfc] = action  
        # print(next_state)   
        return next_state

    def goal_test(self, state):
        if self.find_unfilled_cell(state) != -1:
            return False
        
        for i in range(81):
            if self.isSafe(state, i, state[i]) == False:
                return False
        
        return True

#Test States
# initial_state = [5,0,1,4,6,0,0,0,3,0,7,0,0,0,0,6,0,0,6,8,9,0,3,7,2,4,0,1,0,0,3,4,8,7,0,9,9,0,7,5,2,1,0,0,0,2,3,8,9,7,0,5,0,0,8,0,0,7,0,3,1,0,0,3,9,5,0,1,2,4,0,0,7,0,2,0,5,4,0,0,0]
# prb_state = [0, 0, 1, 1, 0, 3, 1, 2, 3, 6, 9, 0, 0, 0, 7, 0, 0, 7, 0, 3, 2, 6, 8, 9, 6, 8, 9, 0, 0, 3, 9, 1, 7, 0, 3, 4, 0, 5, 0,4, 8, 0, 0, 0, 7, 0, 8, 9, 0, 5, 6, 6, 0, 9, 0, 2, 3, 2, 0, 4, 0, 4, 2, 0, 0, 0, 0, 1, 7, 1, 5, 7, 0, 0, 9, 6, 8, 0, 8, 6, 9]

class SudokuInstrumentedProblem(Problem):
    """Delegates to the Sudoku problem, and keeps statistics."""

    def __init__(self, problem):
        self.problem = problem
        self.succs = self.goal_tests = self.states = 0
        self.found = None

    def actions(self, state):
        self.succs += 1
        return self.problem.actions(state)

    def result(self, state, action):
        self.states += 1
        return self.problem.result(state, action)

    def goal_test(self, state):
        self.goal_tests += 1
        result = self.problem.goal_test(state)
        if result:
            self.found = state
        return result

    def path_cost(self, c, state1, action, state2):
        return self.problem.path_cost(c, state1, action, state2)

    def value(self, state):
        return self.problem.value(state)

    def __getattr__(self, attr):
        return getattr(self.problem, attr)

    def __repr__(self):
        strn =  '<{:4d}/{:4d}/{:4d}>'.format(self.succs, self.goal_tests,
                                               self.states)
        # strn += printMatrix(self.found)
        return strn

def compare_sudoku_searchers(problems, searchers= [ breadth_first_tree_search,
                                                    depth_first_tree_search,
                                                    depth_limited_search,
                                                    iterative_deepening_search]):
    def do(searcher, problem):
        p = SudokuInstrumentedProblem(problem)
        searcher(p)
        print(p)          #For printing the solution after every step
        return p
    
    slen = len(searchers)
    plen = len(problems)
    avg_succs = [0 for i in range(slen)]
    avg_goal_tests = [0 for i in range(slen)]
    avg_states = [0 for i in range(slen)]
    avg_times = []

    data = []
    for s in searchers:
        tmp = []
        time_start = process_time()
        print("Performing ",name(s),"...")
        for p in problems:
            print(".", end="")
            tmp.append(do(s,p))
        print()
        time_end = process_time()
        data.append(tmp)

        avg_times.append((time_end - time_start) / plen)

    for k in range(slen): 
        avg_succs[k] = sum([data[k][i].succs for i in range(plen)]) // plen 
        avg_goal_tests[k] = sum([data[k][i].goal_tests for i in range(plen)]) // plen 
        avg_states[k] = sum([data[k][i].states for i in range(plen)]) // plen

    return [avg_succs, avg_goal_tests, avg_states, avg_times]

test_state = [1,0,0,0,0,7,0,9,0,0,3,0,0,2,0,0,0,8,0,0,9,6,0,0,5,0,0,0,0,5,3,0,0,9,0,0,0,1,0,0,8,0,0,0,2,6,0,0,0,0,4,0,0,0,3,0,0,0,0,0,0,1,0,0,4,0,0,0,0,0,0,7,0,0,7,0,0,0,3,0,0]
hard_state = [0,0,5,3,0,0,0,0,0,8,0,0,0,0,0,0,2,0,0,7,0,0,1,0,5,0,0,4,0,0,0,0,5,3,0,0,0,1,0,0,7,0,0,0,6,0,0,3,2,0,0,0,8,0,0,6,0,5,0,0,0,0,9,0,0,4,0,0,0,0,3,0,0,0,0,0,0,9,7,0,0]

sud_state = [5, 0, 0, 0, 0, 0, 0, 8, 0,
       0, 0, 6, 3, 1, 0, 7, 5, 0,
       1, 0, 0, 7, 0, 0, 0, 9, 0,
       0, 0, 0, 0, 0, 6, 0, 7, 0,
       0, 7, 9, 0, 0, 0, 2, 6, 0,
       0, 5, 0, 8, 0, 0, 0, 0, 0,
       0, 1, 0, 0, 0, 9, 0, 0, 7,
       0, 8, 2, 0, 3, 4, 6, 0, 0,
       0, 6, 0, 0, 0, 0, 0, 0, 3]

# sud = SudokuProblem(sud_state)
# p = SudokuInstrumentedProblem(sud)
# dls = depth_limited_search(p)
# # dfs = breadth_first_tree_search(p)
# print(p)

# easy_data = compare_sudoku_searchers([SudokuProblem(i) for i in [test_state]])
# print(easy_data)

if __name__ == "__main__":
    f = open("instances.txt","r")
    f2 = open("data.txt", "w")
    dic = {}
    jsonString = f.read()
    dic = json.loads(jsonString)
    print("\nAnalysing Easy Data ....\n")
    easy_data = compare_sudoku_searchers([SudokuProblem(i) for i in dic["easy"]], searchers=[breadth_first_tree_search,
                                                                                             depth_first_tree_search,
                                                                                             depth_limited_search])
    print("\nAnalysing Medium Data ....\n")
    medium_data = compare_sudoku_searchers([SudokuProblem(i) for i in dic["medium"]], searchers=[breadth_first_tree_search,
                                                                                                 depth_first_tree_search,
                                                                                                 depth_limited_search])
    print("\nAnalysing Hard Data ....\n")
    hard_data = compare_sudoku_searchers([SudokuProblem(i) for i in dic["hard"]], searchers=[breadth_first_tree_search,
                                                                                             depth_first_tree_search,
                                                                                             depth_limited_search])  # , searchers=[breadth_first_tree_search,depth_first_tree_search,depth_limited_search])
    # print(total_data)
    total_dic = {}
    total_dic["easy"] = easy_data
    total_dic["medium"] = medium_data
    total_dic["hard"] = hard_data
    str1 =  json.dumps(total_dic)
    f2.write(str1)

#Debugging code    
# def debug():
#     as1 = [
#         [5, 2, 1, 4, 6, 9, 8, 7, 3],
#         [4, 7, 3, 2, 8, 5, 6, 9, 1],
#         [6, 8, 9, 1, 3, 7, 2, 4, 5],
#         [1, 5, 6, 3, 4, 8, 7, 2, 9],
#         [9, 4, 7, 5, 2, 1, 3, 8, 6],
#         [2, 3, 8, 9, 7, 6, 5, 1, 4],
#         [8, 6, 4, 7, 9, 3, 1, 5, 2],
#         [3, 9, 5, 8, 1, 2, 4, 6, 7],
#         [7, 1, 2, 6, 5, 4, 9, 3, 8]
#     ]

#     as2 = [
#         5, 2, 1, 4, 6, 9, 8, 7, 3,
#         4, 7, 3, 2, 8, 5, 6, 9, 1,
#         6, 8, 9, 1, 3, 7, 2, 4, 5,
#         1, 5, 6, 3, 4, 8, 7, 2, 9,
#         9, 4, 7, 5, 2, 1, 3, 8, 6,
#         2, 3, 8, 9, 7, 6, 5, 1, 4,
#         8, 6, 4, 7, 9, 3, 1, 5, 2,
#         3, 9, 5, 8, 1, 2, 4, 6, 7,
#         7, 1, 2, 6, 5, 4, 9, 3, 8
#     ]


#     def isSafe(state, ind, k):  # r,c,k):
#         i = -9
#         #Check Up
#         while(ind + i > -1):
#             if state[ind + i] == k:
#                 print("UP")
#                 return False
#             i -= 9

#         i = 9
#         #Check Down
#         while(ind + i < 81):
#             if state[ind + i] == k:
#                 print("DOWN")
#                 return False
#             i += 9

#         #Check right
#         for i in range(1,9 - ind % 9):
#             if state[ind + i] == k:
#                 print("RIGHT")
#                 return False

#         #Check left
#         for i in range(-1, ind%9 * -1 - 1, -1):
#             if state[ind + i] == k:
#                 print("LEFT")
#                 return False

#         return True


#     def goal_test(state):

#         for i in range(81):
#             if isSafe(state, i, state[i]) == False:
#                 return False

#         return True

#     def check(mat):
#         dic1, dic2 = {},{}
#         for i in range(len(mat)):
#             for j in range(len(mat)):
#                 # print("CHECK ROW - ", mat[i][j])
#                 if mat[i][j] not in dic1:
#                     dic1[mat[i][j]] = 1
#                 else:
#                     # print("ROW", i,j,dic1, mat[i][j])
#                     return False
#                 # print("CHECK COL", mat[j][i])
#                 if mat[j][i] not in dic2:
#                     dic2[mat[j][i]] = 1
#                 else:
#                     # print("COL", j, i, dic2, mat[i][j])
#                     return False
#             dic1.clear()
#             dic2.clear()
#         return True

#     # print(check(ass))
#     # print(goal_test(ass1))

    # avg_succs[s] = sum([ans[s][i].succs for i in range(plen)]) // plen
    # avg_goals_tests[s] = sum([ans[s][i].goal_tests for i in range(plen)]) // plen
    # avg_states[s] = sum([ans[s][i].states for i in range(plen)]) // plen

# table = [[name(s)] + [do(s, p) for p in problems] for s in searchers]
# print_table(table, header)
# print("Initial State")
# print(printMatrix(_state))
# sud = SudokuProblem(prb_state)
# compare_sudoku_searchers([sud], header=["Searches", "Values\t\t\tSolved State"])
# p = InstrumentedProblem(sud)
# bfs = breadth_first_tree_search(p)
# print(p)
# # printMatrix(initial_state)
# # print()
# # printMatrix(bfs.state)
# p = InstrumentedProblem(sud)
# dfs = depth_first_tree_search(p)
# # print(p)
# # print()
# # printMatrix(dfs.state)
# p = InstrumentedProblem(sud)
# dls = depth_limited_search(p)
# p = InstrumentedProblem(sud)
# ids = iterative_deepening_search(p)
# print()


dic2 = {}
dic2[0] = [0, 1, 2, 9, 10, 11, 18, 19, 20]
dic2[1] = [3, 4, 5, 12, 13, 14, 21, 22, 23]
dic2[2] = [6, 7, 8, 15, 16, 17, 24, 25, 26]
dic2[3] = [27, 28, 29, 36, 37, 38, 45, 46, 47]
dic2[4] = [30, 31, 32, 39, 40, 41, 48, 49, 50]
dic2[5] = [33, 34, 35, 42, 43, 44, 51, 52, 53]
dic2[6] = [54, 55, 56, 63, 64, 65, 72, 73, 74]
dic2[7] = [57, 58, 59, 66, 67, 68, 75, 76, 77]
dic2[8] = [60, 61, 62, 69, 70, 71, 78, 79, 80]
