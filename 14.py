import sys
import re
from functools import reduce

with open("input/" + (sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3]) + ".in") as file:
    data = file.readlines()

data = [line.split(" ") for line in data]
data = [[tuple(map(int, re.findall(r"-?\d+", part))) for part in line]
        for line in data]
X = 101
Y = 103


def mean(values):
    return sum(values) / len(values)


def var(values):
    return sum((xi - mean(values)) ** 2 for xi in values) / len(values)


def argmin(values):
    return min(range(len(values)), key=lambda i: values[i])


def pos_at_t(t):
    new_positions = []
    for p, v in data:
        x, y = p
        vx, vy = v
        new_x, new_y = (x + t*vx) % X, (y + t*vy) % Y
        new_positions.append((new_x, new_y))
    return new_positions


def draw_positions(positions):
    for y in range(Y):
        for x in range(X):
            if (x, y) not in positions:
                print(" ", end="")
            else:
                print(positions.count((x, y)), end="")
        print()


new_positions = pos_at_t(100)
quadrant_counts = [0, 0, 0, 0]
for new_x, new_y in new_positions:
    if new_x < X//2:
        if new_y < Y//2:
            quadrant_counts[0] += 1
        elif new_y > Y//2:
            quadrant_counts[2] += 1
    elif new_x > X//2:
        if new_y < Y//2:
            quadrant_counts[1] += 1
        elif new_y > Y//2:
            quadrant_counts[3] += 1

print(reduce(lambda x, y: x*y, quadrant_counts, 1))


var_prods = []
for t in range(10000):
    new_positions = pos_at_t(t)

    x_var = var([pos[0] for pos in new_positions])
    y_var = var([pos[1] for pos in new_positions])
    var_prods.append(x_var*y_var)

maybe_tree = argmin(var_prods)
draw_positions(pos_at_t(maybe_tree))
print(maybe_tree)
