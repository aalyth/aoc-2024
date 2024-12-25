#!/usr/bin/env python3


class Operation:
    lhs: str
    rhs: str
    opr: str
    dst: str

    def __init__(self, line: str):
        # x00 AND y00 -> z00
        # lhs opr rhs -> dst
        split = line.split()
        self.lhs = split[0]
        self.opr = split[1]
        self.rhs = split[2]
        self.dst = split[4]

    def compute(self, inputs: dict[str, int]) -> int:
        match self.opr:
            case "AND":
                return inputs[self.lhs] & inputs[self.rhs]
            case "OR":
                return inputs[self.lhs] | inputs[self.rhs]
            case "XOR":
                return inputs[self.lhs] ^ inputs[self.rhs]
        print("reached an invalid case")
        return 0

    def __repr__(self) -> str:
        return f"{self.lhs} {self.opr} {self.rhs} -> {self.dst}"


def parse_input(inp_raw: [str]) -> (dict[str, int], set[Operation]):
    split_idx = inp_raw.index("\n")
    inputs = {}
    for line in inp_raw[:split_idx]:
        split = line.strip().split(":")
        inputs[split[0]] = int(split[1])

    gates = set()
    for line in inp_raw[split_idx + 1 :]:
        gates.add(Operation(line.strip()))

    return (inputs, gates)


def compute_result(inputs: dict[str, int], gates: set[Operation]) -> int:
    target_len = len(inputs) + len(gates)
    while len(inputs) < target_len:
        for gate in gates:
            if gate.dst in inputs:
                continue
            if gate.lhs in inputs and gate.rhs in inputs:
                inputs[gate.dst] = gate.compute(inputs)
    z_gates = sorted(list(filter(lambda wire: wire[0] == "z", inputs.keys())))
    result = 0
    for gate in z_gates[::-1]:
        result = (result << 1) | inputs[gate]
    return result


# opr, lhs, rhs
def gates_to_lookup(
    gates: set[Operation],
) -> (dict[(str, str, str), str], dict[str, [(str, str, str)]]):
    result = {}
    inverse = {}
    for gate in gates:
        result[(gate.opr, gate.lhs, gate.rhs)] = gate.dst
        result[(gate.opr, gate.rhs, gate.lhs)] = gate.dst

        inverse[gate.dst] = [
            (gate.opr, gate.lhs, gate.rhs),
            (gate.opr, gate.rhs, gate.lhs),
        ]
    return result, inverse


# esentially untangle a full adder
def get_swapped_wires(
    gates_lookup: dict[(str, str), dict[str, str]],
    inverse: dict[str, [(str, str, str)]],
) -> str:
    carry = gates_lookup[("AND", "x00", "y00")]
    print(f"previous carry: {carry}")
    a = "x01"
    b = "y01"

    swaps = set([])
    for i in range(1, 38):
        a = f"x{i:02}"
        b = f"y{i:02}"
        z = f"z{i:02}"
        a_xor_b = gates_lookup["XOR", a, b]
        axb_xor_carry = gates_lookup["XOR", a_xor_b, carry]
        print(f"out: {axb_xor_carry}")

        if axb_xor_carry != z:
            gates_lookup["XOR", a_xor_b, carry] = z
            gates_lookup["XOR", carry, a_xor_b] = z

            inv = inverse[z]
            gates_lookup[inv[0]] = axb_xor_carry
            gates_lookup[inv[1]] = axb_xor_carry

            swaps.add(axb_xor_carry)
            swaps.add(z)
            axb_xor_carry = z
            print(f"valid out: {axb_xor_carry}")
            print(f"swaps: {swaps}")
        a_and_b = gates_lookup["AND", a, b]
        axb_and_carry = gates_lookup["AND", a_xor_b, carry]
        axbc_or_ab = gates_lookup["OR", axb_and_carry, a_and_b]
        print(f"new carry: {axbc_or_ab}")

        carry = axbc_or_ab

    # used the code below to debug the final two swaps:

    # carry = "z45"
    # for i in range(44, 37, -1):
    #     a = f"x{i:02}"
    #     b = f"y{i:02}"
    #     z = f"z{i:02}"

    #     a_xor_b = gates_lookup["XOR", a, b]
    #     a_and_b = gates_lookup["AND", a, b]
    #     print(a_xor_b)
    #     print(a_and_b)

    #     axb_and_carry = "".join(set(inverse[carry][0]) - {"OR"} - {a_and_b})
    #     print(f"axb_and_carry:  {axb_and_carry}")

    #     carry = "".join(set(inverse[axb_and_carry][0]) - {"AND"} - {a_xor_b})
    #     print(f"new carry: {carry}")
    #     out = gates_lookup["XOR", a_xor_b, carry]
    #     print(f"out: {out}")

    swaps.add("btb")
    swaps.add("mwp")

    return ",".join(sorted(list(swaps)))


if __name__ == "__main__":
    inp_raw: [str]
    with open("./input.txt", "r") as file:
        inp_raw = file.readlines()
    inputs, gates = parse_input(inp_raw)
    print(compute_result(inputs, gates))
    lookup, inverse = gates_to_lookup(gates)
    print(get_swapped_wires(lookup, inverse))
