import sys

with open("input/" + (sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in")) as file:
    data = file.readlines()


data = [line.split(": ")for line in data]
data = [tuple(part.strip().split()
              for part in line)for line in data]
data = [(int(res[0]), tuple(map(int, ops))) for res, ops in data]

part1 = 0
results_A = {}
results_B = {}


def build_eq_A(cur, i, operands, expected):
    if i < len(operands):
        build_eq_A(cur*operands[i], i+1, operands, expected)
        build_eq_A(cur+operands[i], i+1, operands, expected)
    else:
        if cur == expected:
            results_A[operands] = cur


def build_eq_B(cur, i, operands, expected):
    if i < len(operands):
        build_eq_B(cur*operands[i], i+1, operands, expected)
        build_eq_B(cur+operands[i], i+1, operands, expected)
        # op == || : concatenate operands
        build_eq_B(
            int(str(cur)+str(operands[i])), i+1, operands, expected)
    else:
        if cur == expected:
            results_B[operands] = cur


for index, (expected, operands) in enumerate(data):
    build_eq_A(operands[0], 1, operands, expected)
    build_eq_B(operands[0], 1, operands, expected)

print(sum(results_A.values()))
print(sum(results_B.values()))
