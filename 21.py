from functools import cache
import re
import sys

with open("input/" + (sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in")) as file:
    data = file.readlines()
data = [row.strip() for row in data]

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

    # grouping all steps of the same direction is always better
    vert = "v"*dr+"^"*-dr
    horiz = ">"*dc+"<"*-dc

    if dc > 0 and (rr, c) in pad_dict.values():  # doing vertical first is best, when moving right
        return vert+horiz+"A"
    elif (r, cc) in pad_dict.values():  # else horizontal first ist best if possible
        return horiz+vert+"A"
    elif (rr, c) in pad_dict.values():
        return vert+horiz+"A"

    assert False


@cache
def min_length_for(code, limit=2, depth=0):
    if depth > limit:
        return len(code)

    start = "A"
    sequences = []
    for button in code:
        step = get_step(start, button, depth == 0)
        sequences.append(step)
        start = button

    # Do it per button, smaller sequence --> better caching.
    # All deeper sequnce parts start and end on "A", therefore this is possible.
    return sum(min_length_for(button_sequence, limit, depth+1) for button_sequence in sequences)


def solve(code, limit=2):
    res = min_length_for(code, limit)
    res = res*int(re.findall(r"\d+", code)[0])
    return res


part1 = 0
part2 = 0
for code in data:
    part1 += solve(code)
    part2 += solve(code, 25)
print(part1)
print(part2)
