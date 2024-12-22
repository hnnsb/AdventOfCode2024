import sys

with open("input/" + (sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in")) as file:
    data = file.read()

files = [int(c) for i, c in enumerate(data) if i % 2 == 0]
spaces = [int(c) for i, c in enumerate(data) if i % 2 == 1]

# Part 1
# Build memory layout
layout = []
i = 0
while i < len(files):
    layout += [i] * files[i]
    if i < len(spaces):
        layout += ["."] * spaces[i]

    i += 1

# Move Data
j = -1
i = 0
stop = False
while i < len(layout)+j:
    if layout[i] == ".":
        while layout[j] == ".":
            j -= 1
            if i >= len(layout)+j:
                stop = True
        if stop == True:
            break
        layout[i] = layout[j]
        layout[j] = "."
    i += 1
print(sum([i*c for i, c in enumerate(layout[:i])]))

# Part 2
# Build compacted memory layout
layout = []
id = 0
for i, v in enumerate(data):
    if i % 2 == 0:
        layout.append((int(v), id))
        id += 1
    else:
        layout.append((int(v), -1))

# Try to move whole memory blocks
i = len(layout)-1
while i >= 1:
    if layout[i][1] == -1:
        i -= 1
        continue
    for j in range(i):
        # Look for the next free block
        if layout[j][1] != -1:
            continue
        space, _ = layout[j]

        # Check if enough space
        if space >= layout[i][0]:
            new_space = space - layout[i][0]
            layout[j] = layout[i]
            layout[i] = (layout[j][0], -1)

            # Insert remaining space
            if new_space > 0:
                layout.insert(j+1, (new_space, -1))
                i += 1  # adjust index because of insertion
            break
    i -= 1

# Expand memory layout for calculation
expanded_layout = []
for l, id in layout:
    if l > 0:
        for i in range(l):
            if id == -1:
                id = 0
            expanded_layout.append(id)

print(sum([i*c for i, c in enumerate(expanded_layout)]))
