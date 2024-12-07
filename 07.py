import sys

with open(sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in") as file:
    data = file.readlines()


data = [line.split(": ")for line in data]
data = [tuple(part.strip().split()
              for part in line)for line in data]

part1 = 0
results_A = {}
results_B = {}


def build_eq_recursively_A(cur, i, operands, expected):
    if i < len(operands):
        build_eq_recursively_A(
            eval(str(cur)+"*"+operands[i]), i+1, operands, expected)
        build_eq_recursively_A(
            eval(str(cur)+"+"+operands[i]), i+1, operands, expected)
    else:
        if cur == int(expected):
            results_A[operands] = cur


def build_eq_recursively_B(cur, i, operands, expected):
    if i < len(operands):
        build_eq_recursively_B(
            eval(str(cur)+"*"+operands[i]), i+1, operands, expected)
        build_eq_recursively_B(
            eval(str(cur)+"+"+operands[i]), i+1, operands, expected)
        # op == || : concatenate operands
        build_eq_recursively_B(
            int(str(cur)+operands[i]), i+1, operands, expected)
    else:
        if cur == int(expected):
            results_B[operands] = cur


for index, (expected, operands) in enumerate(data):
    if index % 10 == 0:
        print(index, index/len(data))

    build_eq_recursively_A(operands[0], 1, tuple(
        operands), expected[0])
    build_eq_recursively_B(operands[0], 1, tuple(
        operands), expected[0])


print(sum(results_A.values()))
print(sum(results_B.values()))
