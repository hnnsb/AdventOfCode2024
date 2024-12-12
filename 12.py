import sys
from collections import defaultdict

with open(sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in") as file:
    data = file.readlines()

data = [list(line.strip()) for line in data]
Rows = len(data)
Cols = len(data[0])

dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def find_plot(typ, cur, plot, perim):
    plot.add(cur)
    r, c = cur
    for dr, dc in dirs:
        rr, cc = r+dr, c+dc
        if (rr, cc) not in plot and 0 <= rr < Rows and 0 <= cc < Cols and data[rr][cc] == typ:
            find_plot(typ, (rr, cc), plot, perim)

        if (rr, cc) not in plot and (not (0 <= rr < Rows) or not (0 <= cc < Cols) or data[rr][cc] != typ):
            perim[(dr, dc)].add((rr, cc))
    return plot, perim


def dfs(node):
    stack = [node]
    while stack:
        r, c = stack.pop()
        if (r, c) not in seen_perim:
            seen_perim.add((r, c))
            for dr, dc in dirs:
                rr, cc = r+dr, c+dc
                if (rr, cc) in edges:
                    stack.append((rr, cc))


part1 = 0
part2 = 0
seen = set()
for r in range(Rows):
    for c in range(Cols):
        t = data[r][c]
        if (r, c) in seen:
            continue

        plot, perim = find_plot(t, (r, c), set(), defaultdict(set))
        seen = seen.union(plot)
        perimeter, area = sum(len(v) for v in perim.values()), len(plot)

        # Number of sides is the sum of connected components in each side
        side_count = 0
        for (dr, dc), edges in perim.items():
            seen_perim = set()
            comps = 0
            # For each node, find connected component, if not part of previous component
            for edge_node in edges:
                if edge_node not in seen_perim:
                    comps += 1
                    dfs(edge_node)
            side_count += comps

        part1 += perimeter*area
        part2 += side_count*area

print(part1)
print(part2)
