from functools import cache
import sys
from math import log10, floor

with open(sys.argv[2] if len(sys.argv) > 2 else sys.argv[0][-5:-3] + ".in") as file:
    data = file.read()

stones = list(map(int, data.strip().split(" ")))


@cache
def split_number(stone):
    length = floor(log10(stone)) + 1
    return (stone // (10**(length//2)),
            stone % (10**(length//2)))


@cache
def blink_stone(stone, step):
    if step == 0:
        return 1
    elif stone == 0:
        return blink_stone(1, step-1)
    elif floor(log10(stone)-1) % 2 == 0:
        a, b = split_number(stone)
        return blink_stone(a, step-1) + blink_stone(b, step-1)
    else:
        return blink_stone(stone*2024, step-1)


part1 = 0
part2 = 0
for stone in stones:
    part1 += blink_stone(stone, 25)
    part2 += blink_stone(stone, 75)

print(part1)
print(part2)
