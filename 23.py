from collections import defaultdict
from itertools import combinations
import sys

with open("input/" + (sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in")) as file:
    pairs = file.readlines()
pairs = set([tuple(line.strip().split("-")) for line in pairs])
computers = list(set([c for pair in pairs for c in pair]))
N = len(computers)
adj = defaultdict(list)
for a, b in pairs:
    adj[a].append(b)
    adj[b].append(a)
del a, b
part1 = 0

three_cliques = []
for a, b, c in combinations(computers, 3):
    if b in adj[a] and c in adj[b] and a in adj[c]:
        three_cliques.append({a, b, c})
        if "t" == a[0] or "t" == b[0] or "t" == c[0]:
            part1 += 1

print(part1)

# Extend three cliques as long as possible and save the best (largest=)
best = {}
for clique in three_cliques:
    prev_len = 0
    while len(clique) > prev_len:  # While clique grows
        prev_len = len(clique)
        candidates = set()
        for node in clique:  # Find all nodes that are adjacent to nodes of clique
            if len(candidates) == 0:
                candidates = set(adj[node])
            else:
                candidates.intersection_update(adj[node])
        candidates = candidates-clique  # Remove nodes already in clique
        if len(candidates) > 0:  # If there are any candiates add one to clique
            clique.add(candidates.pop())

    if len(clique) > len(best):  # save the largest clique
        best = clique


print(",".join(sorted(best)))
