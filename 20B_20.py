from copy import copy
from collections import Counter, defaultdict
import sys
from helper.grid import *
import heapq
from copy import deepcopy

with open(sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in") as file:
    data = file.read()

debug = False
if debug:
    data = """
    #####
    #...#
    #.#.#
    #S#.#
    ###.#
    ###.#
    #E#.#
    #.#.#
    #...#
    #####
    """

data = data.split()


grid = [list(row.strip()) for row in data]
maze = NDMatrix(grid)
R, C = maze.dim

for r in range(R):
    for c in range(C):
        if maze[r, c] == "S":
            start = r, c
            maze[r, c] = "."
        if maze[r, c] == "E":
            end = r, c
            maze[r, c] = "."


def print_maze(maze, path):
    m = deepcopy(maze.data)
    for i, (r, c) in enumerate(path):
        m[r][c] = f"{i % 100:02d}"
    for r in range(len(m)):
        for c in range(len(m[0])):
            if m[r][c] == "#":
                m[r][c] = "# "
            if m[r][c] == ".":
                m[r][c] = "  "
    print_matrix(m)


seen = set()
score_from_here = {}
r, c, path = *start, [start]
while (r, c) != end:
    for next_r, next_c in maze.neighbours(r, c):
        if (next_r, next_c) not in seen and maze[next_r, next_c] == ".":
            r, c = next_r, next_c
            path.append((r, c))
            seen.add((r, c))
            break

score_to_here = {node: i for i, node in enumerate(path)}
score_from_here = {node: i for i, node in enumerate(reversed(path))}
base_score = score_to_here[end]

print(base_score)

MAX_DEPTH = 20
if debug:
    MAX_DEPTH = 2


THRESHOLD = 100
if len(sys.argv) > 1:
    THRESHOLD = 50
if debug:
    THRESHOLD = 1

diffs = []
cheats = defaultdict(set)
part2 = 0
R, C = maze.dim
for r, c in path:
    for dr in range(-20, 21):
        for dc in range(-20, 21):
            if abs(dr)+abs(dc) > 20:
                continue

            if maze.inBounds(r+dr, c+dc) and maze[r+dr, c+dc] == ".":
                cheat_length = abs(dr)+abs(dc)
                new_score = score_to_here[r, c] + cheat_length + score_from_here[r+dr, c+dc]
                diff = base_score-new_score
                if diff >= THRESHOLD:
                    part2 += 1
print(part2)
