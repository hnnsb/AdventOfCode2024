import sys
import numpy as np
import re

with open(sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in") as file:
    data = file.readlines()

data = np.array([np.array(list(*line.strip().split())) for line in data])

lines = []
n, m = data.shape
assert n == m

for i in range(n):  # Add cols and rows
    lines.append(data[i, :])
    lines.append(data[:, i])

for i in range(n):  # Add Top-Left to Bottom-Right diagonals
    diag1 = np.array([data[j, i+j] for j in range(n) if i+j < n])
    diag2 = np.array([data[i+j, j] for j in range(n) if i+j < n])
    lines.append(diag1)
    if i > 0:
        lines.append(diag2)


for i in range(n):  # Add Bottom-Left to Top-Right diagonals
    diag3 = np.array([data[n-1-j, i+j]
                     for j in range(n) if n-1-j >= 0 and i+j < n])
    diag4 = np.array([data[n-1-i-j, j] for j in range(n) if n-1-i-j >= 0])
    lines.append(diag3)
    if i > 0:
        lines.append(diag4)

part1 = 0
for line in lines:
    word = "".join(line)
    part1 += len(re.findall(r"(?=(XMAS|SAMX))", word))

print(part1)

part2 = 0
for row in range(1, n-1):
    for col in range(1, m-1):
        if data[row, col] == "A":
            diag1 = set([data[row+1, col+1], data[row-1, col-1]])
            diag2 = set([data[row-1, col+1], data[row+1, col-1]])
            if set(["M", "S"]) == diag1 and set(["M", "S"]) == diag2:
                part2 += 1

print(part2)
