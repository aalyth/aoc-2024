#!/bin/python3

import re


class Coords:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: "Coords") -> "Coords":
        return Coords(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Coords") -> "Coords":
        return Coords(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: int) -> "Coords":
        return Coords(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: int) -> "Coords":
        return Coords(self.x * scalar, self.y * scalar)

    def __mod__(self, other: "Coords") -> "Coords":
        return Coords(self.x % other.x, self.y % other.y)

    def __floordiv__(self, other: "Coords") -> "Coords":
        return Coords(self.x // other.x, self.y // other.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, other: "Coords") -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: "Coords") -> bool:
        return self.x != other.x or self.y != other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class Arcade:
    a: Coords
    b: Coords
    prize: Coords

    def __init__(self, a: Coords, b: Coords, prize: Coords):
        self.a = a
        self.b = b
        self.prize = prize

    def __repr__(self):
        return f"<Arcade: A: {self.a}, B: {self.b}, Prize: {self.prize}>"


def parse_input(inp: [int]) -> [Arcade]:
    result = []
    while len(inp) > 0:
        result.append(
            Arcade(
                Coords(inp.pop(0), inp.pop(0)),
                Coords(inp.pop(0), inp.pop(0)),
                # Coords(inp.pop(0), inp.pop(0)),
                Coords(10000000000000 + inp.pop(0), 10000000000000 + inp.pop(0)),
            )
        )
    return result


def get_arcade_tokens(arcade: Arcade) -> int:
    for i in range(101):
        remaining_dist = arcade.prize - i * arcade.a
        b_diff = remaining_dist // arcade.b
        if remaining_dist % arcade.b == Coords(0, 0) and b_diff.x == b_diff.y:
            return i * 3 + b_diff.x
    return 0


def get_arcade_tokens_ext(arcade: Arcade) -> int:
    # Esentially express the wole arcade as an equation. For example:
    # <Arcade: A: (50, 14), B: (16, 62), Prize: (2112, 994)>
    # x(50,14) + y(16,62) = (2112, 994)
    #
    # 50x + 16y = 2112
    # 14x + 62y = 994
    #
    # Transform to matrix, solve and get the result:
    # A: 40 B: 7

    matrix = [
        [arcade.a.x, arcade.b.x, arcade.prize.x],
        [arcade.a.y, arcade.b.y, arcade.prize.y],
    ]

    for i in range(3):
        matrix[0][i] /= arcade.a.x

    for i in range(3):
        matrix[1][i] -= matrix[0][i] * arcade.a.y

    coef = matrix[1][1]
    for i in range(3):
        matrix[1][i] /= coef

    coef = matrix[0][1]
    for i in range(3):
        matrix[0][i] -= coef * matrix[1][i]

    a_moves = matrix[0][2]
    b_moves = matrix[1][2]
    precision = 0.01
    if (
        abs(a_moves - round(a_moves)) < precision
        and abs(b_moves - round(b_moves)) < precision
    ):
        return int(a_moves * 3 + b_moves)
    return 0


def get_min_tokens(arcades: [Arcade]) -> int:
    return sum(map(get_arcade_tokens_ext, arcades))


if __name__ == "__main__":
    inpRaw: [str]
    with open("./input.txt", "r") as file:
        inpRaw = file.readlines()
    inp = re.findall(r"\d+", str(inpRaw))
    inp = list(map(int, inp))
    arcades = parse_input(inp)
    print(get_min_tokens(arcades))
