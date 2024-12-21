import pulp as pl
import sys
import re
import numpy as np

debug = len(sys.argv) > 1
with open("input/" + (sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3]) + ".in") as file:
    data = file.read()
data = data.split("\n\n")


def parse_coors(button):
    return tuple(map(int, re.findall(r"\d+", button)))


part1 = 0
for claw in data:
    a, b, prize = (parse_coors(x) for x in claw.split("\n"))
    x1 = pl.LpVariable("a_count", 0, 100, 'Integer')
    x2 = pl.LpVariable("b_count", 0, 100, 'Integer')

    model = pl.LpProblem("model", pl.LpMinimize)
    model.setObjective(3*x1+1*x2)
    model += (a[0]*x1+b[0]*x2 == prize[0])
    model += (a[1]*x1+b[1]*x2 == prize[1])
    pl.getSolver("PULP_CBC_CMD", msg=0).solve(model)
    if model.status == 1:
        part1 += model.objective.value()

print(int(part1))


def almost_equal(a, b, e=0.01):
    return abs(a - b) <= e or 1-e <= abs(a-b) <= 1


part2 = 0
part2_lin = 0
for index, claw in enumerate(data):
    a, b, prize = (parse_coors(x) for x in claw.split("\n"))
    prize = (prize[0]+10000000000000, prize[1]+10000000000000)

    n1 = (prize[0]*b[1] - prize[1]*b[0]) / (a[0]*b[1] - a[1]*b[0])
    n2 = (prize[1]*a[0] - prize[0]*a[1]) / (a[0]*b[1] - a[1]*b[0])

    A = np.array([a, b], dtype=np.int64).T
    y = np.array(prize, dtype=np.int64)
    n1_lin, n2_lin = np.linalg.solve(A, y)

    if n1 % 1 == 0 and n2 % 1 == 0 and int(n1) >= 0 and int(n2) >= 0:
        if debug:
            print(index, n1, n2, 3*n1 + n2, sep="\t")
        part2 += (3*n1 + n2)

    if abs(n1_lin-np.round(n1_lin)) <= 0.01 and abs(n2_lin-np.round(n2_lin)) <= 0.01:
        part2_lin += (3*round(n1_lin) + round(n2_lin))

print("Part 2 manual:", int(part2), sep="\t")
print("Part 2 Numpy:", int(part2_lin), sep="\t")
