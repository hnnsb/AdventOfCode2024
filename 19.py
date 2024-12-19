import sys
from helper.grid import *

with open(sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in") as file:
    data = file.read()
patterns, designs = data.split("\n\n")
patterns = set(patterns.split(", "))
designs = designs.split()


def isPossibleNaive(design):
    n = len(design)
    Q = [0]
    while Q:
        start = Q.pop()
        if start == n:
            return True

        for end in range(start+1, n+1):
            if design[start:end] in patterns:
                Q.append(end)

    return False


def isPossibleDP(design, stop=True):
    n = len(design)
    DP = [False] * (n+1)
    DP[0] = True
    for i in range(1, n+1):
        for j in range(i):
            if DP[j] and design[j:i] in patterns:
                DP[i] = True
                break

    return DP[n]


def isPossibleCount(design, stop=True):
    n = len(design)
    DP = [0] * (n+1)
    DP[0] = 1
    for i in range(1, n+1):
        for j in range(i):
            if design[j:i] in patterns:
                DP[i] += DP[j]

    return DP[n]


part1 = 0
part2 = 0
for i, design in enumerate(designs):
    p = isPossibleCount(design)
    part1 += p > 0
    part2 += p

print(part1)
print(part2)
