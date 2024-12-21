import sys
import heapq
from copy import deepcopy
from more_itertools import flatten
from helper.grid import DIRS, print_matrix

with open("input/" + (sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3]) + ".in") as file:
    data = file.readlines()
maze = [list(line.strip()) for line in data]


def print_maze(maze, path):
    m = deepcopy(maze)
    for r, c in path:
        m[r][c] = "O"
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if m[r][c] == ".":
                m[r][c] = " "
    print_matrix(m)
    print()


R = len(maze)
C = len(maze[0])

for r in range(R):
    for c in range(C):
        if maze[r][c] == "S":
            start = (r, c)
            maze[r][c] = "."
        if maze[r][c] == "E":
            end = (r, c)
            maze[r][c] = "."

cur_dir = 2
seen = set()
Q = [(0, *start, cur_dir, [], 0)]
depths = {}
best = 1e6
best_path = []
while Q:
    score, r, c, cur_dir, path, depth = heapq.heappop(Q)

    if (r, c) == end and score <= best:
        best = score
        best_path = path
        # Don't stop after finding the goal, but keep exploring to find the costs to every cell

    if (r, c, cur_dir) in seen:
        continue

    depths[(r, c, cur_dir)] = depth  # Remember how many steps it took to get here
    seen.add((r, c, cur_dir))

    dr, dc = DIRS[cur_dir]
    next_r, next_c = r+dr, c+dc
    if maze[next_r][next_c] == ".":
        heapq.heappush(Q, (score + 1, next_r, next_c, cur_dir, path+[(r, c)], depth+1))
    heapq.heappush(Q, (score + 1000, r, c, (cur_dir+1) % 4, path+[(r, c)], depth+1))
    heapq.heappush(Q, (score + 1000, r, c, (cur_dir+3) % 4, path+[(r, c)], depth+1))

print("--- Part 1 ---")
# print_maze(maze, best_path)
print(best)

# Part 2
paths = []


def build_path(r, c, cur_dir, path, score):
    """
    Explore possible paths recursively. If a paths score matches the best path, 
    it is another option of best paths.
    """
    if (r, c) == end and score == best:
        paths.append(path)

    # Make each move that is possible from the current position.
    for i, (dr, dc) in enumerate(DIRS):
        new_dir = i
        if new_dir != cur_dir and (r, c, cur_dir) in depths and depths[(r, c, cur_dir)] + 1 == depths[(r, c, new_dir)]:
            build_path(r, c, i, path+[(r, c)], score+1000)

    dr, dc = DIRS[cur_dir]
    next_r, next_c = r+dr, c+dc
    if (next_r, next_c, cur_dir) in depths and depths[(r, c, cur_dir)]+1 == depths[(next_r, next_c, cur_dir)]:
        build_path(next_r, next_c, cur_dir, path+[(next_r, next_c)], score+1)


print("--- Part 2 ---")
build_path(*start, 2, [start], 0)
# print_maze(maze, flatten(paths))
print(len(set(flatten(paths))))  # Unique cells in any path
