import sys
import re
with open(sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in") as file:
    data = file.read()
registers_, program = data.split("\n\n")
registers_ = re.findall(r"\d+", registers_)
program = "".join(re.findall(r"\d+", program))
register_names = ["A", "B", "C"]
registers = {key: int(value) for key, value in zip(register_names, registers_)}


def solve(registers, program: str, part2=False, verbose=False):
    p = 0
    res = []

    def combo(operand):
        assert operand != 7
        if operand > 3:
            return registers[register_names[operand-4]]
        return operand

    while p < len(program):
        if part2:
            if res[len(res)-1] != program[len(res)-1]:
                return r, None

        opcode, operand = int(program[p]), int(program[p+1])

        if opcode == 0:  # adv
            registers["A"] = int(registers["A"] / int(1 << combo(operand)))  # 2^n == 1<<n

        elif opcode == 1:  # bxl
            registers["B"] = registers["B"] ^ operand

        elif opcode == 2:  # bst
            registers["B"] = combo(operand) % 8

        elif opcode == 3:  # jnz
            if registers["A"] != 0:
                p = operand
                continue

        elif opcode == 4:  # bxc
            registers["B"] = registers["B"] ^ registers["C"]

        elif opcode == 5:  # out
            for c in str(combo(operand) % 8):
                res.append(c)
            if verbose:
                print(*str(combo(operand) % 8), end=",")

        elif opcode == 6:  # bdv
            registers["B"] = registers["A"] // int(1 << combo(operand))  # 2^n == 1<<n

        elif opcode == 7:  # cdv
            registers["C"] = registers["A"] // int(1 << combo(operand))  # 2^n == 1<<n

        p += 2

    if verbose:
        print()
    return res, registers


r, rs = solve(registers, program)
print(",".join(r))
