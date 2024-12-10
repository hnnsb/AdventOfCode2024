import sys

with open(sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in") as file:
    data = file.readlines()
data = [list(line.strip()) for line in data]
data = [list(map(int, line)) for line in data]

Rows = len(data)
Cols = len(data[0])
trailheads = [(r, c) for r in range(Rows)
              for c in range(Cols) if data[r][c] == 0]

dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def traverse(cur, path):
    r, c = cur
    path.append(cur)
    if data[r][c] == 9:
        paths.append(path)
        return  # Stop recursion when at height 9
    for dr, dc in dirs:
        next_r, next_c = r+dr, c+dc
        if 0 <= next_r < Rows and 0 <= next_c < Cols:
            if data[next_r][next_c]-1 == data[r][c]:
                traverse((next_r, next_c), path[:])


part1 = 0
part2 = 0

for start in trailheads:
    paths = []
    traverse(start, [])
    part1 += len(set([path[-1] for path in paths]))
    part2 += len(paths)

print(part1)
print(part2)
