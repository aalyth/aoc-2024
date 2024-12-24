#!/bin/python3

import heapq


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

    def __neg__(self) -> "Coords":
        return Coords(-self.x, -self.y)

    def __mul__(self, scalar: int) -> "Coords":
        return Coords(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: int) -> "Coords":
        return Coords(self.x * scalar, self.y * scalar)

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

    trivial: bool

    def __init__(self, trivial=False):
        self.data = []
        self.trivial = trivial

    def push(self, value: any):
        if self.trivial:
            self.data.append(value)
        else:
            heapq.heappush(self.data, value)

    def pop(self) -> any:
        return self.data.pop(0)

    def is_empty(self) -> bool:
        return len(self.data) == 0


class BfsEntry:
    node: Coords
    dist: int

    def __init__(self, node: Coords, dist: int) -> None:
        self.node = node
        self.dist = dist

    def __lt__(self, other) -> bool:
        return self.dist < other.dist


def find_tile(field: [[str]], tile: str) -> Coords:
    for y in range(len(field)):
        for x in range(len(field[0])):
            if field[y][x] == tile:
                return Coords(x, y)
    return Coords(0, 0)


DIRECTIONS = [Coords(1, 0), Coords(-1, 0), Coords(0, 1), Coords(0, -1)]


# for some reason does not work on first case, but gets the star
def mark_shortest_paths(
    field: [[str]], start: Coords, end: Coords
) -> dict[Coords, int]:
    distances: dict[Coords, int] = {start: 0}
    bfs_queue = Queue()

    bfs_queue.push(BfsEntry(start, 0))
    while not bfs_queue.is_empty():
        entry = bfs_queue.pop()

        for direction in DIRECTIONS:
            tmp = entry.node + direction
            if not tmp.valid(field) or field[tmp.y][tmp.x] == "#":
                continue

            next_dist = entry.dist + 1

            if tmp not in distances:
                distances[tmp] = next_dist
                bfs_queue.push(BfsEntry(tmp, next_dist))
            elif next_dist < distances[tmp]:
                distances[tmp] = next_dist
                bfs_queue.push(BfsEntry(tmp, next_dist))

    return distances


# legacy code for the first star
def get_cheat_numbers(field: [[str]]) -> int:
    start = find_tile(field, "S")
    end = find_tile(field, "E")
    distances = mark_shortest_paths(field, start, end)

    queue = Queue(trivial=True)
    traversed: set[Coords] = set([start])

    result = 0
    arr = []
    queue.push(start)
    while not queue.is_empty():
        node = queue.pop()

        for direction in DIRECTIONS:
            tmp = node + direction
            if not tmp.valid(field):
                continue

            if field[tmp.y][tmp.x] == "#":
                for dir_ in DIRECTIONS:
                    jump = tmp + dir_

                    if jump.valid(field) and field[jump.y][jump.x] != "#":
                        dist = distances[jump] - distances[node] - 2
                        if dist >= 100:
                            result += 1

                continue

            if tmp not in traversed:
                traversed.add(tmp)
                queue.push(tmp)

    return result


def count_cheats(field: [[str]], allowed_cheats: int) -> int:
    start = find_tile(field, "S")
    end = find_tile(field, "E")
    distances = mark_shortest_paths(field, start, end)

    queue = Queue(trivial=True)
    traversed: set[Coords] = set([start])

    queue.push(start)
    result = 0
    res = []
    while not queue.is_empty():
        node = queue.pop()

        for radius in range(1, allowed_cheats + 1):
            for offset in range(radius):
                inverse = radius - offset

                points = [
                    node + Coords(offset, inverse),
                    node + Coords(inverse, -offset),
                    node + Coords(-offset, -inverse),
                    node + Coords(-inverse, offset),
                ]

                for point in points:
                    if not point.valid(field) or field[point.y][point.x] == "#":
                        continue

                    manhattan_distance = abs(node.x - point.x) + abs(node.y - point.y)
                    dist = distances[node] - distances[point] - manhattan_distance

                    if dist >= 100:
                        result += 1

        for direction in DIRECTIONS:
            tmp = node + direction
            if not tmp.valid(field):
                continue

            if field[tmp.y][tmp.x] == "#":
                continue

            if tmp not in traversed:
                traversed.add(tmp)
                queue.push(tmp)

    return result


if __name__ == "__main__":
    inp_raw: [str]
    with open("./input.txt", "r") as file:
        inp_raw = file.readlines()
    field = [list(line.strip()) for line in inp_raw]
    print(count_cheats(field, 20))
