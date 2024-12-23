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
        # self.data.append(value)
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


DIRECTIONS = [Coords(1, 0), Coords(-1, 0), Coords(0, 1), Coords(0, -1)]


# for some reason does not work on first case, but gets the star
def mark_shortest_paths(field: [[str]], start: Coords, end: Coords) -> int:
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

    if end not in distances:
        return -1
    return distances[end]


FIELD_SIZE = 71
APPLIED_BYTES = 1024

if __name__ == "__main__":
    inp_raw: [str]
    with open("./input.txt", "r") as file:
        inp_raw = file.readlines()
    falling_bytes = [
        Coords(int(line.split(",")[0]), int(line.split(",")[1])) for line in inp_raw
    ]

    field = [["."] * FIELD_SIZE for _ in range(FIELD_SIZE)]
    for i in range(APPLIED_BYTES):
        byte = falling_bytes[i]
        field[byte.y][byte.x] = "#"
    print(
        mark_shortest_paths(field, Coords(0, 0), Coords(FIELD_SIZE - 1, FIELD_SIZE - 1))
    )

    falling_bytes = falling_bytes[APPLIED_BYTES:]
    for byte in falling_bytes:
        field[byte.y][byte.x] = "#"
        if -1 == mark_shortest_paths(
            field, Coords(0, 0), Coords(FIELD_SIZE - 1, FIELD_SIZE - 1)
        ):
            print(byte)
            break
