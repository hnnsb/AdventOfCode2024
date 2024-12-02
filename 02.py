with open("02.in") as file:
    data = file.readlines()
data = [line.split() for line in data]
data = [list(map(int, line)) for line in data]
    
def isSafe(line):
    descending = all(line[i] > line[i+1] for i in range(len(line)-1))
    ascending = all(line[i] < line[i+1] for i in range(len(line)-1))
    good_diffs = all(1 <= abs(line[i] - line[i+1]) <= 3 for i in range(len(line)-1))
    return (descending or ascending) and good_diffs
    
part1 = 0
part2 = 0
for line in data:    
    if isSafe(line):
        part1 += 1
    
    for i in range(len(line)+1): # Check leaving each one out, +1 to check whole list.
        new_line = line[:i] + line[i+1:]
        if isSafe(new_line):
            part2 +=1
            break # Save time if we find one that is safe
        
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")