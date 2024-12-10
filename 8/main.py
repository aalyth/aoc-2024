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


def build_node_buckets(field: [[str]]) -> dict[str, list[Coords]]:
    node_buckets: dict[str, list[Coords]] = dict()
    for y in range(len(field)):
        for x in range(len(field[y])):
            tile: str = field[y][x]
            if tile != ".":
                if tile not in node_buckets:
                    node_buckets[tile] = [Coords(x, y)]
                else:
                    node_buckets[tile].append(Coords(x, y))
    return node_buckets


def count_antinodes(field: [[str]]) -> int:
    node_buckets = build_node_buckets(field)

    for bucket in node_buckets.values():
        print(bucket)
        for lnode in bucket:
            for rnode in bucket:
                if lnode == rnode:
                    continue

                antinode = lnode - (rnode - lnode)
                if antinode.valid(field):
                    field[antinode.y][antinode.x] = "#"

    antinodes_count = 0
    for row in field:
        for tile in row:
            if tile == "#":
                antinodes_count += 1

    return antinodes_count


def count_antinodes_ext(field: [[str]]) -> int:
    node_buckets = build_node_buckets(field)

    for bucket in node_buckets.values():
        print(bucket)
        for lnode in bucket:
            for rnode in bucket:
                if lnode == rnode:
                    continue

                diff = rnode - lnode
                antinode = lnode
                while antinode.valid(field):
                    field[antinode.y][antinode.x] = "#"
                    antinode -= diff

    antinodes_count = 0
    for row in field:
        print(*row)
        for tile in row:
            if tile == "#":
                antinodes_count += 1

    return antinodes_count


if __name__ == "__main__":
    inp: [str]
    with open("./input.txt", "r") as file:
        inp = file.readlines()
    inp = [list(line.strip()) for line in inp]
    print(count_antinodes_ext(inp))
    print("hello")
