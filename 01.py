import sys 

with open(sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][:2] + ".in") as file:
    data = file.readlines()
    
data = [line.split() for line in data]
data = [list(map(int, line)) for line in data]
data = list(zip(*data))
a,b = [list(s) for s in data]

a, b = sorted(a), sorted(b)
part1 = 0
for i in range(len(a)):
    d = abs(a[i]-b[i])
    part1 += d
print(part1)
    
part2 = 0 
for e in a:
    part2 += e * b.count(e)
print(part2)