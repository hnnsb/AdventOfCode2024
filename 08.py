import sys
from collections import defaultdict
from itertools import combinations

with open("input/" + (sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in")) as file:
    data = file.readlines()

data = [[*line.strip()] for line in data]
n = len(data)
m = len(data)

antennas = defaultdict(list)

for r, row in enumerate(data):
    for c, cell in enumerate(row):
        if cell != ".":
            antennas[cell] += [(r, c)]

antinodes1 = set()
antinodes2 = set()
for freq, coors in antennas.items():
    c = combinations(coors, 2)
    for a, b in c:
        r1, c1 = a
        r2, c2 = b
        dr = r1-r2
        dc = c1-c2

        for i in range(max(n, m)):  # iteration range could be more exact but too lazy. Something like "while 0 <= new_r1 < n and ..."
            new_r1 = r1+i*dr
            new_r2 = r2-i*dr
            new_c1 = c1+i*dc
            new_c2 = c2-i*dc

            if i == 1:  # Part 1
                if 0 <= new_r1 < n and 0 <= new_c1 < m:
                    antinodes1.add((new_r1, new_c1))
                if 0 <= new_r2 < n and 0 <= new_c2 < m:
                    antinodes1.add((new_r2, new_c2))

            if 0 <= new_r1 < n and 0 <= new_c1 < m:
                antinodes2.add((new_r1, new_c1))
            if 0 <= new_r2 < n and 0 <= new_c2 < m:
                antinodes2.add((new_r2, new_c2))

print(len(antinodes1))
print(len(antinodes2))
