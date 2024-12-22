from collections import Counter, deque
import sys

with open("input/" + (sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in")) as file:
    data = file.readlines()
data = [int(x) for x in data]


def next_secret(n):
    # ~2.2s cumulative time
    res = n*64
    n = (n ^ res) % 16777216
    res = n//32
    n = (n ^ res) % 16777216
    res = n*2048
    n = (n ^ res) % 16777216
    return n


def optimized_next_secret(n):
    # ~1.6s cumulative time
    n = (n ^ (n << 6)) & 0xFFFFFF
    n = (n ^ (n >> 5)) & 0xFFFFFF
    n = (n ^ (n << 11)) & 0xFFFFFF
    return n


def simulate(n):
    seq_to_price = dict()
    diffs = deque(maxlen=4)
    prev_price = n % 10
    for i in range(2000):
        n = optimized_next_secret(n)

        price = n % 10
        diff = price-prev_price
        diffs.append(diff)
        key = tuple(diffs)
        if i > 4 and key not in seq_to_price:  # Remember price at first occurence of sequence
            seq_to_price[key] = price

        prev_price = price

    return n, seq_to_price


prices_for_seqs = Counter()
part1 = 0
for num in data:
    res, seq_to_price = simulate(num)
    prices_for_seqs += Counter(seq_to_price)  # Sum up the prices for each sequence
    part1 += res

print(part1)
print(prices_for_seqs.most_common(1)[0][1])  # The highest price for all sequences
