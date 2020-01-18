
from random import *

n = 3
goal = {}
for i in range(1, 10):
    goal[i] = i
goal[9] = '-'

def user_fill(board):
    used = {}
    print('enter the values of tiles numbered from 1 to 8')
    for i in range(1,9):
        x = int(input(str(i)+': '))
        while x in used or x not in [1, 2, 3, 4, 5, 6, 7, 8]:
            print("Invalid input.")
            x = int(input(str(i)+': '))
        board[i] = x;
        used[x] = 1;

    board[9] = '-'
def random_fill(board):
    used = {}
    for i in range(1, 9):
        x = randint(1, 8)
        while x in used:
            x = randint(1, 8)
        used[x] = 1
        board[i] = x
    board[9] = '-'
def get_inversion(board):

    inversion = 0
    for i in range(1, 10):
        if board[i] == '-':
             continue;
        for j in range(i+1, 10):
            if board[j] == '-':
                 continue;
            if board[i] > board[j]:
                inversion +=1

    return inversion
def solvable(board):
    inversion = get_inversion(board)
    return inversion % 2 == 0

def print_board(board):
    print('--------------')
    for i in range(1, 10, 3):
        print(board[i], board[i+1], board[i+2])
    #print('--------------')
def get_neighbours(board, adj, gap):
    ret = []
    #print("in get_neighbours")
    #print_board(board)
    #print('gap', gap)
    for n in adj[gap]:
        #print("-----------------")
        board[gap], board[n] = board[n], board[gap]
        #print_board(board)
        #print("-----------------")
        ret.append(dict(board))
        board[gap], board[n] = board[n], board[gap]

    return ret
#
def is_solved(board, goal):
    return board == goal

#
def find_gap(board):
    # print('in find_gap')
    #print_board(board)
    for i in range(1, 10):
        if board[i] == '-':
            return i

    return -1
#
def print_path(path):
    print('path is ')
    for node in path:
        print_board(node)

#takes a dictionary representing board, and returns a tuple representing that board
def hashed(board):
    ret = []
    for k, v in board.items():
        ret.append(v)
    return tuple(ret)

# takes hashed tuple of values and return a dictionary representing the board
def unhashed(hashed_board):
    ret = {}
    for i in range(len(hashed_board)):
        ret[i+1] = hashed_board[i]
    return ret

def trace_path(parent, start):
    rev_path = [start]
    hashed_start = hashed(start)
    while parent[hashed_start] is not None :
        unhashed_board = unhashed(parent[hashed_start])
        rev_path.append(unhashed_board)
        hashed_start = parent[hashed_start]

    return rev_path[::-1]

#solved using bfs, return solution path
def bfs_solve(board,adj, path):
    if board == goal:
        return path

    gap = find_gap(board)
    frontier = []
    parent = {hashed(board): None}
    visited = {hashed(board): 1}

    frontier.append(board)

    while len(frontier) > 0:
        front = frontier.pop(0)
        print_board(front)
        hashed_front = hashed(front)
        #if reached goal, trace path using parent pointers
        if front == goal:
            path = trace_path(parent, front)
            return path

        gap = find_gap(front)
        neighbours = get_neighbours(front, adj, gap)

        for neighbour in neighbours:
            hash_n = hashed(neighbour)
            if hash_n not in visited:
                visited[hash_n] = 1
                parent[hash_n] = hashed(front)
                frontier.append(neighbour)


#solved using backtracking and heurestics based on inversions count
def solve_puzzle(board, adj, gap, visited, path):
    if board == goal:
        print_path(path)
        return True
    neighbours = get_neighbours(board, adj, gap)
    oldinv = get_inversion(board)
    for n in neighbours:
        hash_n = hashed(n)
        inv = get_inversion(n);
        if hash_n not in visited and oldinv >= inv:
            print('oldinv, inv')
            print(oldinv, inv)
            print_board(n)
            visited[hash_n] = 1
            path.append(dict(n))
            new_gap = find_gap(n)
            ans = solve_puzzle(n, adj, new_gap, visited, path)
            if ans == True:
                return True
            path.pop(-1)

def get_path():

    board = {}
    visited = {}
    adj = {1: (2, 4), 2 : (1, 3, 5), 3 : (2, 6), 4 : (1, 5, 7), 5 : (2, 4, 6, 8), 6 : (5, 3, 9),
           7 : (4, 8), 8 : (7, 5, 9), 9 : (8, 6)}

    while True:
        random_fill(board)
        if solvable(board) :
            break;

    path = [board]
    # board = dict(goal)
    gap = 9

    print_board(board)
    #solve_puzzle(board, adj, gap, visited, path)
    path = bfs_solve(board, adj, path)

    return path

def get_path_from_user():
    board = {}
    visited = {}
    adj = {1: (2, 4), 2 : (1, 3, 5), 3 : (2, 6), 4 : (1, 5, 7), 5 : (2, 4, 6, 8), 6 : (5, 3, 9),
           7 : (4, 8), 8 : (7, 5, 9), 9 : (8, 6)}

    user_fill(board)
    if not solvable(board) :
            #print("Not Solvable: Try initial state with even number of inversions")
            raise ValueError("Not Solvable: Try initial state with even number of inversions")

    path = [board]

    gap = 9

    print_board(board)
    print('1. Solve using BFS 2. Solve using backtracking')
    choice = input()
    while True:
        if choice == '1':
            path = bfs_solve(board, adj, path)
            print_path(path)
            return path
        if choice == '2':
            solve_puzzle(board, adj, gap, visited, path)
            return path
        else:
            print('Invalid choice. Enter 1 or 2')
            choice = input()
