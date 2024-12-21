import sys
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
seen = dict()
Q = [(0, *start, cur_dir, [start])]
paths = []
while Q:
    score, r, c, cur_dir, path = Q.pop(0)

    if (r, c) == end:
        paths.append((path, score))
        continue

    if (r, c, cur_dir) in seen and seen[(r, c, cur_dir)] < score:
        continue

    seen[(r, c, cur_dir)] = score

    dr, dc = DIRS[cur_dir]
    next_r, next_c = r+dr, c+dc
    if maze[next_r][next_c] == ".":
        Q.append((score + 1, next_r, next_c, cur_dir, path+[(next_r, next_c)]))
    Q.append((score + 1000, r, c, (cur_dir+1) % 4, path))
    Q.append((score + 1000, r, c, (cur_dir+3) % 4, path))

print("--- Part 1 ---")
best_score = min(paths, key=lambda x: x[1])[1]
print(best_score)

# Part 2
print("--- Part 2 ---")
best_paths = map(lambda x: x[0], filter(lambda x: x[1] == best_score, paths))
# print_maze(maze, flatten(paths))
print(len(set(flatten(best_paths))))  # Unique cells in any path
