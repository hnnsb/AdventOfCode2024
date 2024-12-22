import sys
import re

with open("input/" + (sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in")) as file:
    data = file.read()

part1 = 0
for match in re.findall(r"mul\(\d+,\d+\)", data):
    numbers = match[4:-1]
    a, b = map(int, numbers.split(","))
    part1 += a * b

print(part1)

part2 = 0
do = True
for match in re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", data):
    if match.startswith("don't()"):
        do = False
    elif match.startswith("do()"):
        do = True
    elif do:
        numbers = match[4:-1]
        a, b = map(int, numbers.split(","))
        part2 += a * b

print(part2)
