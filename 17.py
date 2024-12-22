import sys
import re
with open("input/" + (sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in")) as file:
    data = file.read()

register_names = ["A", "B", "C"]

registers, program = data.split("\n\n")
registers = re.findall(r"\d+", registers)
registers = {key: int(value) for key, value in zip(register_names, registers)}
program = [int(x) for x in re.findall(r"\d+", program)]


def solve(registers, program):
    p = 0
    res = []

    def combo(operand):
        assert operand != 7
        if operand > 3:
            return registers[register_names[operand-4]]
        return operand

    while p < len(program):
        opcode, operand = program[p], program[p+1]
        match opcode:
            case 0:  # adv
                registers["A"] = registers["A"] // (1 << combo(operand))  # 2^n == 1<<n
            case 1:  # bxl
                registers["B"] = registers["B"] ^ operand
            case 2:  # bst
                registers["B"] = combo(operand) % 8
            case 3:  # jnz
                if registers["A"] != 0:
                    p = operand
                    continue
            case 4:  # bxc
                registers["B"] = registers["B"] ^ registers["C"]
            case 5:  # out
                res.append(combo(operand) % 8)
            case 6:  # bdv
                registers["B"] = registers["A"] // (1 << combo(operand))  # 2^n == 1<<n
            case 7:  # cdv
                registers["C"] = registers["A"] // (1 << combo(operand))  # 2^n == 1<<n
        p += 2

    return res


r = solve(registers, program)
print(",".join(map(str, r)))

# --- Part 2 ---
# 01: 2,4 B = A%8 ==> B in [0..7]
# 02: 1,3 B = B^3 -> B^0b11
# 03: 7,5 C = A>>B
# 04: 1,5 B = B^5 -> B^0b101
# 05: 0,3 A = A>>3
# 06: 4,3 B = B^C
# 07: 5,5 out += B%8
# 08: 3,0 if A!=0: jmp 00

options = [0]
# Build program from back to front, the first digits of A decide the last digits of the output.
for pos in reversed(range(len(program))):
    new_options = []
    for num in options:
        for offset in range(2**3):
            A = 2**3 * num + offset
            if solve({"A": A, "B": 0, "C": 0}, program) == program[pos:]:  # Compare with the last digits of program
                # A is a valid option
                new_options.append(A)
    options = new_options

print(min(options))
assert min(options) == 236548287712877
