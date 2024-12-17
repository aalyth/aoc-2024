#!/bin/python3

from typing import Union

import heapq

import sys

sys.setrecursionlimit(150000)


class Coords:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

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


def get_start_pos(field: [[str]]) -> Coords:
    for y in range(len(field)):
        for x in range(len(field[0])):
            if field[y][x] == "S":
                return Coords(x, y)
    return Coords(-1, -1)


def get_end_pos(field: [[str]]) -> Coords:
    for y in range(len(field)):
        for x in range(len(field[0])):
            if field[y][x] == "E":
                return Coords(x, y)
    return Coords(-1, -1)


DIRECTIONS = [Coords(1, 0), Coords(-1, 0), Coords(0, 1), Coords(0, -1)]


class BfsEntry:
    node: Coords
    direction: Coords
    dist: int

    def __init__(self, node: Coords, direction: Coords, dist: int) -> None:
        self.node = node
        self.direction = direction
        self.dist = dist

    def __lt__(self, other: "BfsEntry") -> bool:
        return self.dist < other.dist


# for some reason does not work on first case, but gets the star
def mark_shortest_paths(
    field: [[str]], start: Coords, start_dir: Coords, end: Coords
) -> int:
    distances: dict[Coords, int] = {start: 0}
    bfs_queue = Queue()

    prev_direction = start_dir
    bfs_queue.push(BfsEntry(start, prev_direction, 0))
    while not bfs_queue.is_empty():
        entry = bfs_queue.pop()

        for direction in DIRECTIONS:
            tmp = entry.node + direction
            if field[tmp.y][tmp.x] == "#":
                continue

            next_dist = entry.dist + 1
            if direction != entry.direction:
                next_dist += 1000

            if tmp not in distances:
                distances[tmp] = next_dist
                bfs_queue.push(BfsEntry(tmp, direction, next_dist))
            elif next_dist < distances[tmp]:
                distances[tmp] = next_dist
                bfs_queue.push(BfsEntry(tmp, direction, next_dist))

    return distances[end]


def count_shortest_paths(
    field: [[str]], start: Coords, spf_len: int, end: Coords
) -> int:
    distances: dict[Coords, int] = {start: 0}
    traversed: set[Coords] = set()
    bfs_queue = Queue()

    prev_direction = Coords(1, 0)
    bfs_queue.push(BfsEntry(start, prev_direction, 0))
    while not bfs_queue.is_empty():
        entry = bfs_queue.pop()

        for direction in DIRECTIONS:
            tmp = entry.node + direction
            if field[tmp.y][tmp.x] == "#":
                continue

            if tmp in traversed:
                continue

            next_dist = entry.dist + 1
            if direction != entry.direction:
                next_dist += 1000

            if next_dist > spf_len:
                continue

            end_dist = mark_shortest_paths(field, tmp, direction, end)
            if next_dist + end_dist == spf_len:
                print(f"adding: {tmp}")
                traversed.add(tmp)
            elif next_dist + end_dist > spf_len:
                continue

            if tmp not in distances:
                distances[tmp] = next_dist
                bfs_queue.push(BfsEntry(tmp, direction, next_dist))
            elif next_dist < distances[tmp]:
                distances[tmp] = next_dist
                bfs_queue.push(BfsEntry(tmp, direction, next_dist))

    return len(traversed) + 1


def get_shortest_path(field: [[str]]) -> int:
    start_pos = get_start_pos(field)
    end_pos = get_end_pos(field)
    spf_s = mark_shortest_paths(field, start_pos, Coords(1, 0), end_pos)
    print(f"count: {count_shortest_paths(field, start_pos, spf_s, end_pos)}")
    return spf_s


if __name__ == "__main__":
    inp_raw: [str]
    with open("./input.txt", "r") as file:
        inp_raw = file.readlines()
    field = [list(line.strip()) for line in inp_raw]
    print(get_shortest_path(field))
