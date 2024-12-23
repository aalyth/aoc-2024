#!/bin/python3


class Computer:
    reg_a: int
    reg_b: int
    reg_c: int

    ip: int

    def __init__(self, reg_a: int, reg_b: int, reg_c: int) -> None:
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_c = reg_c
        self.ip = 0

    def get_arg(self, operand: int) -> int:
        match operand:
            case 4:
                return self.reg_a
            case 5:
                return self.reg_b
            case 6:
                return self.reg_c
            case 7:
                return 0
        return operand

    def exec_instr(self, instr: int, operand: int) -> None:
        arg = self.get_arg(operand)
        match instr:
            case 0:  # adv
                self.reg_a >>= arg
            case 1:  # bxl
                self.reg_b ^= operand
            case 2:  # bst
                self.reg_b = arg & 0x7
            case 3:  # jnz
                if self.reg_a != 0:
                    self.ip = arg
                    return
            case 4:  # bxc
                self.reg_b ^= self.reg_c
            case 5:  # out
                print(f"{arg & 0x7},", end="")
            case 6:  # bdv
                self.reg_b = self.reg_a >> arg
            case 7:  # bdv
                self.reg_c = self.reg_a >> arg
        self.ip += 2

    def execute(self, program: [int]) -> None:
        self.ip = 0
        while self.ip < len(program):
            self.exec_instr(program[self.ip], program[self.ip + 1])
        print("\b ")

    def __repr__(self) -> str:
        return f"({self.reg_a}, {self.reg_b}, {self.reg_c})"


def get_equation_solutions(a: int, n: int) -> [int]:
    res = []
    for i in range(8):
        if n == ((a & 0x7 ^ 4) ^ (a >> (a & 0x7 ^ 1))) & 0x7:
            res.append(i)
        a += 1
    return res


def find_a(prog: [int], a=0) -> int:
    if len(prog) == 0:
        return a

    el = prog[-1]

    a <<= 3
    solutions = get_equation_solutions(a, el)
    if len(solutions) == 0:
        return -1

    for sol in solutions:
        tmp = find_a(prog[:-1], a | sol)
        if tmp != -1:
            return tmp

    return -1


if __name__ == "__main__":
    inp_raw: [str]
    with open("./input.txt", "r") as file:
        inp_raw = file.readlines()
    reg_a = int(inp_raw[0].split(":")[1])
    reg_b = int(inp_raw[1].split(":")[1])
    reg_c = int(inp_raw[2].split(":")[1])
    prog = list(map(int, inp_raw[4].split(":")[1].split(",")))
    c = Computer(reg_a, reg_b, reg_c)
    a = find_a(prog)
    print(a)
    c.reg_a = a
    c.execute(prog)
    # print(c)
