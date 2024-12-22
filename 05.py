import sys
from collections import defaultdict

with open("input/" + (sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in")) as file:
    data = file.read()

rules, updates = data.split("\n\n")
rules = [tuple(map(int, line.split("|"))) for line in rules.split("\n")]
updates = [list(map(int, line.split(","))) for line in updates.split("\n")]
rules_dict = defaultdict(list)
for k, v in rules:
    rules_dict[k] += [v]


def check_order(update):
    for index, page in enumerate(update):
        after = rules_dict[page]
        for other in after:
            other_index = 1e6
            try:
                other_index = update.index(other)
            except:
                pass

            if other_index < index:
                return False
    return True


def correct_order(update):
    applying_rules = list(filter(lambda rule: rule[0] in update, rules))
    update: list = update[:]
    for i in range(len(update)-1):
        for j in range(i+1, len(update)):
            if (update[j], update[i]) in applying_rules:
                update.insert(i, update.pop(j))

    return update


part1 = 0
part2 = 0

for i, update in enumerate(updates):
    if check_order(update):
        part1 += update[len(update)//2]
    else:
        corrected = correct_order(update)
        part2 += corrected[len(corrected)//2]

print(part1)
print(part2)
