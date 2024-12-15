import sys

with open(sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in") as file:
    data = file.read()

debug = False
if debug:
    data = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

warehouse, moves = data.split("\n\n")
warehouse = [list(line) for line in warehouse.split("\n")]
moves = "".join(moves.split("\n"))

warehouse2 = []
for row in warehouse:
    new_row = []
    for c in row:
        if c == "@":
            new_row.append("@")
            new_row.append(".")
        elif c == "O":
            new_row.append("[")
            new_row.append("]")
        else:
            new_row.append(c)
            new_row.append(c)
    warehouse2.append(new_row)

# Part 1
R = len(warehouse)
C = len(warehouse[0])

for r, row in enumerate(warehouse):
    for c, cell in enumerate(row):
        if cell == "@":
            start = (r, c)

dirs = {"<": (0, -1), "^": (-1, 0), ">": (0, 1), "v": (1, 0)}

cur = start
for move in moves:
    dr, dc = dirs[move]
    r, c = cur
    next_r, next_c = r+dr, c+dc
    if warehouse[next_r][next_c] == ".":
        warehouse[next_r][next_c] = "@"
        warehouse[r][c] = "."
        cur = next_r, next_c
    elif warehouse[next_r][next_c] == "#":
        pass
    elif warehouse[next_r][next_c] == "O":
        lookahead = 1
        while warehouse[next_r+lookahead*dr][next_c+lookahead*dc] == "O":
            lookahead += 1
        if warehouse[next_r+lookahead*dr][next_c+lookahead*dc] == ".":
            warehouse[next_r+lookahead*dr][next_c+lookahead*dc] = "O"
            warehouse[next_r][next_c] = "@"
            warehouse[r][c] = "."
            cur = next_r, next_c


def print_matrix(m):
    for row in m:
        print(" ".join(row))


part1 = 0
for r in range(R):
    for c in range(C):
        if warehouse[r][c] == "O":
            part1 += 100*r + c
print(part1)

# Part 2
R = len(warehouse2)
C = len(warehouse2[0])

for r, row in enumerate(warehouse2):
    for c, cell in enumerate(row):
        if cell == "@":
            start = (r, c)


cur = start
for step, move in enumerate(moves):
    dr, dc = dirs[move]
    r, c = cur
    next_r, next_c = r+dr, c+dc
    if warehouse2[next_r][next_c] == ".":
        warehouse2[next_r][next_c] = "@"
        warehouse2[r][c] = "."
        cur = next_r, next_c

    elif warehouse2[next_r][next_c] == "#":
        pass

    elif warehouse2[next_r][next_c] in ["[", "]"]:
        if move in ["<", ">"]:
            lookahead = 1
            while warehouse2[next_r+lookahead*dr][next_c+lookahead*dc] in ["[", "]"]:
                lookahead += 1
            if warehouse2[next_r+lookahead*dr][next_c+lookahead*dc] == ".":
                for i in range(lookahead, 0, -1):
                    warehouse2[next_r+i*dr][next_c+i * dc] = \
                        warehouse2[next_r+(i-1)*dr][next_c+(i-1)*dc]
                warehouse2[next_r][next_c] = "@"
                warehouse2[r][c] = "."
                cur = next_r, next_c
        else:  # Up and down
            # Gather all affected boxes
            other_c = next_c + \
                1 if warehouse2[next_r][next_c] == "[" else next_c-1
            box_layers = [set([(next_r, next_c), (next_r, other_c)])]
            i = 1
            while i <= len(box_layers):
                layer = set()
                for box_r, box_c in box_layers[i-1]:
                    if warehouse2[box_r+dr][box_c] in ["[", "]"]:

                        other_c = box_c + \
                            1 if warehouse2[box_r +
                                            dr][box_c] == "[" else box_c-1
                        layer.add((box_r+dr, box_c))
                        layer.add((box_r+dr, other_c))

                if len(layer) > 0:
                    box_layers.append(layer)
                i += 1

            blocked = any([any(warehouse2[box_r+dr][box_c] ==
                          "#" for box_r, box_c in layer) for layer in box_layers])
            if not blocked:
                # Move Boxes
                for layer in box_layers[::-1]:
                    for box_r, box_c in layer:
                        warehouse2[box_r+dr][box_c +
                                             dc] = warehouse2[box_r][box_c]
                        warehouse2[box_r][box_c] = "."
                warehouse2[next_r][next_c] = "@"
                warehouse2[r][c] = "."
                cur = next_r, next_c

part2 = 0
for r in range(R):
    for c in range(C):
        if warehouse2[r][c] == "[":
            part2 += 100*r + c
print(part2)
