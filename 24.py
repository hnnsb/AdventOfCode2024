import sys
from helper.grid import *

with open("input/" + (sys.argv[1] if len(sys.argv) > 1 else sys.argv[0][-5:-3] + ".in")) as file:
    data = file.read()

inputs, gates = data.split("\n\n")
inputs = [input.split(": ") for input in inputs.splitlines()]
inputs = {wire: bool(int(value)) for wire, value in inputs}
gates = gates.splitlines()

still_running = True
while still_running:
    still_running = False
    for gate in gates:
        operand1, operation, operand2, _, target = gate.split(" ")
        if operand1 in inputs and operand2 in inputs and target not in inputs:
            match operation:
                case "AND":
                    inputs[target] = inputs[operand1] and inputs[operand2]
                case "OR":
                    inputs[target] = inputs[operand1] or inputs[operand2]
                case "XOR":
                    inputs[target] = inputs[operand1] != inputs[operand2]

            still_running = True


res = [(k, v) for k, v in inputs.items() if k.startswith("z")]
res = sorted(res, key=lambda x: x[0])
res = map(lambda x: int(x[1]), res)
part1 = 0
for i, bit in enumerate(res):
    part1 += bit*2**i
print(part1)
