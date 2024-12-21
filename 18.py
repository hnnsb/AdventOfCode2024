import sys
from helper.grid import *
from collections import deque

with open("input/" + (sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3]) + ".in") as file:
    data = file.readlines()

data = [tuple(map(int, line.split(","))) for line in data]

N = 70
ns = 1024
if len(sys.argv) > 1:  # Test Case
    N = 6
    ns = 12


def inBounds(x, y):
    return 0 <= x <= N and 0 <= y <= N


start = (0, 0)
end = (N, N)


def bfs(blocked):
    seen = set()
    blocked = set(blocked)
    Q = deque([(*start, [])])
    while Q:
        x, y, path = Q.popleft()

        if (x, y) == end:
            return True, path

        if (x, y) in seen:
            continue

        seen.add((x, y))
        for dx, dy in DIRS:
            next_x, next_y = x+dx, y+dy
            if (next_x, next_y) not in blocked and inBounds(next_x, next_y):
                Q.append((next_x, next_y, path+[(next_x, next_y)]))

    return False, []


_, path = bfs(data[:ns])
print(len(path))

for n in reversed(range(1, len(data))):
    possible, _ = bfs(data[:n])
    if possible:
        # Not blocked anymore
        # n because where coming from the back and slice data[:n] is exclusive n.
        blocks = data[n]
        print(f"{blocks[0]},{blocks[1]}")
        break
