#!/bin/python3


class Coords:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def valid(self, field: [[str]]) -> bool:
        return (
            self.x >= 0
            and self.x < len(field[0])
            and self.y >= 0
            and self.y < len(field)
        )

    def abs(self) -> "Coords":
        return Coords(abs(self.x), abs(self.y))

    def dot_product(self, other: "Coords") -> "Coords":
        return Coords(self.x * other.x, self.y * other.y)

    def right_rotation(self) -> "Coords":
        ROTATE_RIGHT_MATRIX = [
            [0, 1],
            [-1, 0],
        ]

        return Coords(
            self.x * ROTATE_RIGHT_MATRIX[0][0] + self.y * ROTATE_RIGHT_MATRIX[1][0],
            self.x * ROTATE_RIGHT_MATRIX[0][1] + self.y * ROTATE_RIGHT_MATRIX[1][1],
        )

    def __add__(self, other: "Coords") -> "Coords":
        return Coords(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: "Coords") -> "Coords":
        self = self + other
        return self

    def __sub__(self, other: "Coords") -> "Coords":
        return Coords(self.x - other.x, self.y - other.y)

    def __isub__(self, other: "Coords") -> "Coords":
        self = self - other
        return self

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, other: "Coords") -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: "Coords") -> bool:
        return self.x != other.x or self.y != other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class Queue:
    data: any

    def __init__(self):
        self.data = []

    def push(self, value: any):
        self.data.append(value)

    def pop(self) -> any:
        return self.data.pop(0)

    def is_empty(self) -> bool:
        return len(self.data) == 0


def get_fence_cost(field: [[str]], start: Coords, traversed: set[Coords]) -> (int, int):
    directions = [Coords(-1, 0), Coords(1, 0), Coords(0, -1), Coords(0, 1)]
    plant = field[start.y][start.x]
    queue = Queue()
    queue.push(start)

    traversed_walls: dict[Coords, [Coords]] = dict()

    area = 0
    # the counting of wall boils down to counting the number of corners
    walls = 0
    perimeter = 0
    while not queue.is_empty():
        current = queue.pop()
        if current in traversed:
            continue
        traversed.add(current)
        area += 1

        for direction in directions:
            neighbour = current + direction
            if neighbour.valid(field) and field[neighbour.y][neighbour.x] == plant:
                if neighbour not in traversed:
                    queue.push(neighbour)
            else:
                perimeter += 1
                if current not in traversed_walls:
                    traversed_walls[current] = [direction]
                else:
                    traversed_walls[current].append(direction)

            # check whether it's an internally pointed corner, i.e. the two
            # sides point to a same plant, but the diagonal to a different
            tmp = current + direction.right_rotation()
            diag = current + direction + direction.right_rotation()
            if (
                neighbour.valid(field)
                and field[neighbour.y][neighbour.x] == plant
                and tmp.valid(field)
                and field[tmp.y][tmp.x] == plant
                and diag.valid(field)
                and field[diag.y][diag.x] != plant
            ):
                walls += 1

    # check the outwards facing corners
    for dirs in traversed_walls.values():
        # make sure it's not two opposite sides
        if len(dirs) == 2 and dirs[0].dot_product(Coords(-1, -1)) != dirs[1]:
            walls += 1
        elif len(dirs) == 3:
            walls += 2
        elif len(dirs) == 4:
            walls += 4

    return (area * perimeter, area * walls)


def get_total_fence_cost(field: [[str]]) -> (int, int):
    traversed: set[Coords] = set()

    result = 0
    result_discount = 0
    for y in range(len(field)):
        for x in range(len(field[0])):
            coord = Coords(x, y)
            if coord in traversed:
                continue
            (normal, discounted) = get_fence_cost(field, coord, traversed)
            result += normal
            result_discount += discounted

    return (result, result_discount)


if __name__ == "__main__":
    inp: [str]
    with open("./input.txt", "r") as file:
        inp = file.readlines()
    inp = [list(line.strip()) for line in inp]
    print(get_total_fence_cost(inp))
    print("hello")
