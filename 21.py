from functools import cache
from itertools import permutations
import re
import sys
from helper.grid import *

with open(sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in") as file:
    data = file.readlines()
data = [row.strip() for row in data]

MOVES = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1)
}
number_pad = [['7', '8', '9'],
              ['4', '5', '6'],
              ['1', '2', '3'],
              ['-', '0', 'A']]

arrow_pad = [["-", "^", "A"],
             ["<", "v", ">"]]

number_pad_dict = {v: (i, j) for i, row in enumerate(number_pad) for j, v in enumerate(row) if v != '-'}
arrow_pad_dict = {v: (i, j) for i, row in enumerate(arrow_pad) for j, v in enumerate(row) if v != '-'}


@cache
def get_step(start, end, isNumberPad):
    pad_dict = number_pad_dict if isNumberPad else arrow_pad_dict
    r, c = pad_dict[start]
    rr, cc = pad_dict[end]
    dr = rr-r
    dc = cc-c
    vert = "v"*dr+"^"*-dr
    horiz = ">"*dc+"<"*-dc
    if dc > 0 and (rr, c) in pad_dict.values():
        return vert+horiz+"A"
    elif (r, cc) in pad_dict.values():
        return horiz+vert+"A"
    elif (rr, c) in pad_dict.values():
        return vert+horiz+"A"

    assert False


def min_length_for(code, limit=2, depth=0):
    if depth > limit:
        return len(code)

    start = "A"
    sequence = []
    for button in code:
        seq = get_step(start, button, depth == 0)
        sequence.append(seq)

        start = button

    return min_length_for("".join(sequence), limit, depth+1)


def solve(code, limit=2):
    res = min_length_for(code, limit)
    print(res, " * ", re.findall(r"\d+", code)[0])
    res = res*int(re.findall(r"\d+", code)[0])
    return res


part1 = 0
part2 = 0
for code in data:
    part1 += solve(code)
print(part1)  # too high 190424
exit()
for code in data:
    part2 += solve(code, 25)
print(part2)
