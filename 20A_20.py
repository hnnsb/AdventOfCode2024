from collections import Counter
import sys
from helper.grid import *
import heapq
from copy import deepcopy

with open("input/" + (sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3]) + ".in") as file:
    data = file.read()
# data = """
# #####
# #...#
# #.#.#
# #S#.#
# ###.#
# ###.#
# #E#.#
# #.#.#
# #...#
# #####
# """

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
    for r, c, score in path:
        m[r][c] = f"{score % 100:02d}"
    for r in range(len(m)):
        for c in range(len(m[0])):
            if m[r][c] == "#":
                m[r][c] = "# "
            if m[r][c] == ".":
                m[r][c] = "  "
    print_matrix(m)


seen = set()
Q = [(0, *end, [])]
score_from_here = {}
while Q:
    score, r, c, path = heapq.heappop(Q)

    if (r, c) == start:
        base_score = score

        for r, c, score in path:
            score_from_here[r, c] = score
        break

    if (r, c) in seen:
        continue

    seen.add((r, c))

    for dr, dc in DIRS:
        next_r, next_c = r+dr, c+dc
        if maze[next_r, next_c] == ".":
            heapq.heappush(Q, (score + 1, next_r, next_c, path+[(r, c, score)]))
print(base_score)
path.append((*start, base_score))

part1 = 0
for r, c, score in reversed(path[1:]):
    score_adjusted = base_score-score
    for dr, dc in DIRS:
        next_r, next_c = r+dr, c+dc

        if maze[next_r, next_c] == "#":
            for ddr, ddc in DIRS:
                next_next_r, next_next_c = next_r+ddr, next_c+ddc

                if (next_next_r, next_next_c) != (r, c) and (next_next_r, next_next_c) in score_from_here:
                    diff = base_score - (score_adjusted+2+score_from_here[next_next_r, next_next_c])
                    if diff >= 100:
                        part1 += 1

print(part1)
