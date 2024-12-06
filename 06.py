import time
import sys

with open(sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in") as file:
    data = file.readlines()

data = [[*line.strip()] for line in data]
for r, row in enumerate(data):
    for c, col in enumerate(row):
        if col != "." and col != "#":
            starting = (r, c)
            assert col == "^"
            data[r][c] = "."

n, m = len(data), len(data[0])
dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

dir = 0
guard = starting
visited = set([guard])

while True:
    dr, dc = dirs[dir]
    gr, gc = guard
    tr, tc = gr+dr, gc+dc
    if 0 <= tr < n and 0 <= tc < m:
        if data[tr][tc] == ".":
            guard = tr, tc
            visited.add(guard)
        elif data[tr][tc] == "#":
            dir = (dir + 1) % 4
    else:
        # out of bounds
        break

print(len(visited))

part2 = 0
d1 = time.time()
# 130 * 130 possible positions to add a rock, takes 40 seconds to check all on my machine
for r in range(n):
    for c in range(m):
        if data[r][c] == "#" or (r, c) == starting:
            continue
        dir = 0
        guard = starting
        visited = set([(guard, dir)])
        loop = False
        copy = [row[:] for row in data]
        copy[r][c] = "#"
        while not loop:
            dr, dc = dirs[dir]
            gr, gc = guard
            tr, tc = gr+dr, gc+dc

            if ((tr, tc), dir) in visited:
                loop = True

            if 0 <= tr < n and 0 <= tc < m:
                if copy[tr][tc] == ".":
                    guard = tr, tc
                    visited.add((guard, dir))
                elif copy[tr][tc] == "#":
                    dir = (dir + 1) % 4
            else:
                # out of bounds
                break

        if loop:
            part2 += 1

d2 = time.time()

print(part2)
print(f"Part two took {d2-d1:.2f} seconds")
