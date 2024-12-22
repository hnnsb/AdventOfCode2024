import sys
from helper.grid import *

with open("input/" + (sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in")) as file:
    data = file.read()

warehouse, moves = data.split("\n\n")
warehouse2 = warehouse
moves = "".join(moves.split("\n"))

replacements = [(".", ".."), ("#", "##"), ("@", "@."), ("O", "[]")]
for old, new in replacements:
    warehouse2 = warehouse2.replace(old, new)
warehouse = [list(line) for line in warehouse.split("\n")]
warehouse2 = [list(line) for line in warehouse2.split("\n")]

dirs = {"<": (0, -1), "^": (-1, 0), ">": (0, 1), "v": (1, 0)}


def score(grid, key):
    res = 0
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == key:
                res += 100*r + c
    return res


# Part 1
r, c = find_cell(warehouse, "@")
for move in moves:
    dr, dc = dirs[move]
    next_r, next_c = r+dr, c+dc
    if warehouse[next_r][next_c] == ".":
        warehouse[next_r][next_c] = "@"
        warehouse[r][c] = "."
        r, c = next_r, next_c
    elif warehouse[next_r][next_c] == "O":
        lookahead = 1
        while warehouse[next_r+lookahead*dr][next_c+lookahead*dc] == "O":
            lookahead += 1
        if warehouse[next_r+lookahead*dr][next_c+lookahead*dc] == ".":
            warehouse[next_r+lookahead*dr][next_c+lookahead*dc] = "O"
            warehouse[next_r][next_c] = "@"
            warehouse[r][c] = "."
            r, c = next_r, next_c

print(score(warehouse, "O"))


# Part 2
def collect_affected_boxes(warehouse2, dr, next_r, next_c):
    other_c = next_c + 1 if warehouse2[next_r][next_c] == "[" else next_c-1
    box_layers = [set([(next_r, next_c), (next_r, other_c)])]
    i = 1
    while i <= len(box_layers):
        layer = set()
        for box_r, box_c in box_layers[i-1]:
            if warehouse2[box_r+dr][box_c] in ["[", "]"]:
                other_c = box_c + 1 if warehouse2[box_r + dr][box_c] == "[" else box_c-1
                layer.add((box_r+dr, box_c))
                layer.add((box_r+dr, other_c))

        if len(layer) > 0:
            box_layers.append(layer)
        i += 1
    return box_layers


r, c = find_cell(warehouse2, "@")
for step, move in enumerate(moves):
    dr, dc = dirs[move]
    next_r, next_c = r+dr, c+dc
    if warehouse2[next_r][next_c] == ".":
        warehouse2[next_r][next_c] = "@"
        warehouse2[r][c] = "."
        r, c = next_r, next_c

    elif warehouse2[next_r][next_c] in ["[", "]"]:
        if move in ["<", ">"]:  # Left and right
            lookahead = 1
            while warehouse2[next_r+lookahead*dr][next_c+lookahead*dc] in ["[", "]"]:
                lookahead += 1
            if warehouse2[next_r+lookahead*dr][next_c+lookahead*dc] == ".":
                for i in range(lookahead, 0, -1):
                    warehouse2[next_r + i*dr][next_c + i*dc] = warehouse2[next_r + (i-1)*dr][next_c + (i-1)*dc]
                warehouse2[next_r][next_c] = "@"
                warehouse2[r][c] = "."
                r, c = next_r, next_c

        else:  # Up and down
            affected_boxes = collect_affected_boxes(warehouse2, dr, next_r, next_c)
            blocked = any([any(warehouse2[box_r+dr][box_c] == "#" for box_r, box_c in layer)
                          for layer in affected_boxes])
            if blocked:
                continue

            # Move Boxes
            for layer in reversed(affected_boxes):
                for box_r, box_c in layer:
                    warehouse2[box_r+dr][box_c+dc] = warehouse2[box_r][box_c]
                    warehouse2[box_r][box_c] = "."

            warehouse2[next_r][next_c] = "@"
            warehouse2[r][c] = "."
            r, c = next_r, next_c

print(score(warehouse2, "["))
