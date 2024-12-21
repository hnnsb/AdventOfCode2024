from functools import cache
import sys
import time
from helper.grid import *
from helper.stat import *

with open("input/" + (sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3]) + ".in") as file:
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
    DP = [0] * (n+1)
    DP[0] = 1
    for i in range(1, n+1):
        for j in range(i):
            if design[j:i] in patterns:
                DP[i] += DP[j]

    return DP[n]


@cache
def isPossibleRec(design: str):
    ans = 0
    if not design:
        ans = 1
    for pattern in patterns:
        if design.startswith(pattern):
            ans += isPossibleRec(design[len(pattern):])

    return ans


def run(func, out=False):
    part1 = 0
    part2 = 0
    for design in designs:
        p = func(design)
        part1 += p > 0
        part2 += p

    if out:
        print(part1)
        print(part2)


run(isPossibleDP, True)

# Some evaluation
runTimes = {"DP": [], "Rec": []}

for i in range(10):
    d1 = time.time()
    run(isPossibleDP)
    d2 = time.time()
    isPossibleRec.cache_clear()
    d3 = time.time()
    run(isPossibleRec)
    d4 = time.time()

    runTimes["DP"].append(d2-d1)
    runTimes["Rec"].append(d4-d3)

for k, v in runTimes.items():
    print(f"{k} \t Mean: {mean(v)*1000:.4f} ms, \tvariance: " +
          f"{var(v) * 1000:.4f} ms^2 \tTotal time for {len(v)} iterations: {sum(v)} s")
