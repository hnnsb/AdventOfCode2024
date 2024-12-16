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


class NDMatrix:
    # TODO
    # transpose
    # print for higher dimensions
    # dimension validation
    #
    def __init__(self, data):
        # TODO validate data
        self.data = data

    def __getitem__(self, key):
        if isinstance(key, tuple):
            element = self.data
            for k in key:
                if not isinstance(element, list):
                    raise IndexError(f"Index shape {key} does not match dimension {self.dim}.")
                element = element[k]
            return element
        else:
            return NDMatrix(self.data[key])

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            element = self.data
            for k in key[:-1]:
                if not isinstance(element, list):
                    raise IndexError(f"Index shape {key} does not match dimension {self.dim}.")
                element = element[k]
            element[key[-1]] = value
        else:
            self.data[key] = value

    def __repr__(self):
        return repr(self.data)

    def __str__(self):
        def format_list(lst):
            if isinstance(lst, list):
                return "[" + ", ".join(format_list(sub) if isinstance(sub, list) else str(sub) for sub in lst) + "]"
            return str(lst)

        return "[" + "\n ".join(format_list(row) for row in self.data) + "]"

    @property
    def dim(self):
        def _dimensions(lst):
            if isinstance(lst, list) and lst:
                return [len(lst)] + _dimensions(lst[0])
            return []

        return tuple(_dimensions(self.data))


if __name__ == "__main__":
    l3d = [[[1, 1], [2, 2]],
           [[3, 3], [4, 4]]]
    l = NDMatrix(l3d)
    print(l[1])
    print(l[0, 0, 1])
    print(l.dim)
    print(l)
    print(NDMatrix(l3d[0]))
