DIRS = [(0, -1), (-1, 0), (0, 1), (1, 0)]
"""Left, up, right, down"""
DIRS_DIAG = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
"""Top left, top right, bottom right, bottom left"""
DIRS8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
"""All 8 neighboring directions, also diagonals, in order by row"""


def find_cell(grid, v):
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == v:
                return (r, c)


def print_matrix(m):
    for row in m:
        print(" ".join(row))
