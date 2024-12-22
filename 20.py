import sys
from helper.grid import *
import cProfile

with open("input/" + (sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in")) as file:
    data = file.readlines()

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

THRESHOLD = 100
if len(sys.argv) > 1:
    THRESHOLD = 50


def solve(distance):
    res = 0
    for r, c in path:
        for dr in range(-distance, distance + 1):
            for dc in range(-distance, distance + 1):
                if abs(dr) + abs(dc) > distance or abs(dr) + abs(dc) < 2:
                    continue

                if maze.in_bounds(r + dr, c + dc) and maze[r + dr, c + dc] == ".":
                    cheat_length = abs(dr) + abs(dc)
                    new_score = score_to_here[r, c] + cheat_length + score_from_here[r + dr, c + dc]
                    diff = base_score - new_score
                    if diff >= THRESHOLD:
                        res += 1

    return res


print(solve(2))
# print(solve(20))
cProfile.run("print(solve(20))")
