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
    for r, c, score in path:
        m[r][c] = f"{score%100:02d}"
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
score_from_here[start] = base_score
print_maze(maze, path)

MAX_DEPTH = 20
if debug:
    MAX_DEPTH = 2


def bfs(r, c, depth, seen):
    if depth > MAX_DEPTH:
        return []
    if maze[r, c] == ".":
        return [(r, c)]

    seen.add((r, c))
    ends = []
    for dr, dc in DIRS:
        next_r, next_c = r+dr, c+dc
        if maze.inBounds(r+dr, c+dc) and (next_r, next_c) not in seen:
            ends += bfs(r+dr, c+dc, depth+1, seen)
    return ends


THRESHOLD = 100
if len(sys.argv) > 1:
    THRESHOLD = 50
if debug:
    THRESHOLD = 1

diffs = []
cheats = defaultdict(set)
for r, c, score in reversed(path[1:]):
    score_adjusted = base_score-score
    for dr, dc in DIRS:
        next_r, next_c = r+dr, c+dc
        if maze[next_r, next_c] == "#":
            # TODO start from cell on path not first cheat cell so you can get the so to here,
            # and different starts using the same cheat are differentiated by their start score
            cheat_start = next_r, next_c
            cheat_ends = bfs(next_r, next_c, 0, set([(r, c)]))

            cheats[cheat_start] = cheats[cheat_start].union(set(cheat_ends))

for cheat_start, cheat_ends in cheats.items():
    for cheat_end in cheat_ends:
        dr, dc = abs(cheat_start[0]-cheat_end[0]), abs(cheat_start[1]-cheat_end[1])
        # TODO Score calc, score_adjusted is not right, maybe dict score_to_here
        new_score = score_adjusted + dr+dc + score_from_here[cheat_end]
        diff = base_score-new_score
        if diff >= THRESHOLD:
            diffs.append(diff)

for time, count in sorted(Counter(diffs).items(), key=lambda x: x[1], reverse=True):
    print(count, time)

pass
