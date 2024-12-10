#!/bin/python3

ROTATE_RIGHT_MATRIX = [
    [0, 1],
    [-1, 0],
]


class Coords:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def rotate_right(self):
        x = self.x * ROTATE_RIGHT_MATRIX[0][0] + self.y * ROTATE_RIGHT_MATRIX[1][0]
        y = self.x * ROTATE_RIGHT_MATRIX[0][1] + self.y * ROTATE_RIGHT_MATRIX[1][1]
        self.x = x
        self.y = y

    def valid(self, field: [[str]]) -> bool:
        return (
            self.x >= 0
            and self.x < len(field[0])
            and self.y >= 0
            and self.y < len(field)
        )

    def __add__(self, other: "Coords") -> "Coords":
        return Coords(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: "Coords") -> "Coords":
        self = self + other
        return self

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, other: "Coords") -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: "Coords") -> bool:
        return self.x != other.x or self.y != other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


def find_guard_coords(inp: [str]) -> Coords:
    for i in range(len(inp)):
        for j in range(len(inp[0])):
            if inp[i][j] == "^":
                return Coords(j, i)

    raise ValueError("input does not contain guard")


def mark_guard_path(field: [[str]]) -> [[str]]:
    guard = find_guard_coords(field)
    guard_direction = Coords(0, -1)

    field[guard.y][guard.x] = "X"

    while guard.valid(field):
        tmp = guard + guard_direction
        if not tmp.valid(field):
            break

        if field[tmp.y][tmp.x] == "#":
            guard_direction.rotate_right()
        guard += guard_direction
        field[guard.y][guard.x] = "X"

    return field


def count_guard_path(marked_field: [[str]]) -> int:
    res = 0
    for line in marked_field:
        for ch in line:
            if ch == "X":
                res += 1
    return res


def is_cycle(field: [[str]], guard: Coords, guard_dir: Coords) -> bool:
    traversed: dict[Coords, [Coords]] = dict()
    traversed[guard] = [guard_dir]
    start = guard
    start_dir = guard_dir
    it = 0
    while guard.valid(field) and it < 100000:
        tmp = guard + guard_dir
        if not tmp.valid(field):
            break

        if tmp == start:
            print("returning true")
            return True

        if field[tmp.y][tmp.x] == "#":
            guard_dir.rotate_right()

        guard += guard_dir
        if guard not in traversed:
            traversed[guard] = [guard_dir]
        else:
            traversed[guard].append(guard_dir)
        it += 1

    return False


def count_potential_cycles(field: [[str]]) -> int:
    guard = find_guard_coords(field)
    guard_direction = Coords(0, -1)

    cycles = 0
    traversed_cycles: set[Coords] = set()

    while guard.valid(field):
        tmp = guard + guard_direction
        if not tmp.valid(field):
            break

        if field[tmp.y][tmp.x] == "#":
            guard_direction.rotate_right()
            continue
        guard += guard_direction

        tmp_direction = Coords(guard_direction.x, guard_direction.y)
        tmp_direction.rotate_right()

        prev_tile = field[guard.y][guard.x]
        field[guard.y][guard.x] = "#"

        if guard not in traversed_cycles and is_cycle(field, guard, tmp_direction):
            cycles += 1
            traversed_cycles.add(guard)

        field[guard.y][guard.x] = prev_tile

    # for some reason it should be 1812
    return cycles


if __name__ == "__main__":
    inp: [str]
    with open("./input.txt", "r") as file:
        inp = file.readlines()
    inp = [list(line.strip()) for line in inp]
    # marked = mark_guard_path(inp)
    # print(count_guard_path(marked))
    print(count_potential_cycles(inp))
