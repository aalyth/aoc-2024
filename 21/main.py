#!/usr/bin/env pypy3


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

    def __sub__(self, other: "Coords") -> "Coords":
        return Coords(self.x - other.x, self.y - other.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, other: "Coords") -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: "Coords") -> bool:
        return self.x != other.x or self.y != other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


NUMERIC_KEYS = {
    "7": Coords(0, 0),
    "8": Coords(1, 0),
    "9": Coords(2, 0),
    "4": Coords(0, 1),
    "5": Coords(1, 1),
    "6": Coords(2, 1),
    "1": Coords(0, 2),
    "2": Coords(1, 2),
    "3": Coords(2, 2),
    "X": Coords(0, 3),
    "0": Coords(1, 3),
    "A": Coords(2, 3),
}

DIRECTIONAL_KEYS = {
    "X": Coords(0, 0),
    "^": Coords(1, 0),
    "A": Coords(2, 0),
    "<": Coords(0, 1),
    "v": Coords(1, 1),
    ">": Coords(2, 1),
}


def get_horizontal(diff: Coords) -> str:
    if diff.x < 0:
        return "<" * abs(diff.x)
    return ">" * diff.x


def get_vertical(diff: Coords) -> str:
    if diff.y < 0:
        return "^" * abs(diff.y)
    return "v" * diff.y


def get_path_permutations(pos: Coords, diff: Coords, keys: dict[str, Coords]) -> [str]:
    bad_pos = keys["X"]
    # h - horizontal, v - vertical
    hv = get_horizontal(diff) + get_vertical(diff) + "A"
    vh = get_vertical(diff) + get_horizontal(diff) + "A"
    if pos + Coords(0, diff.y) == bad_pos:
        return [hv]
    if pos + Coords(diff.x, 0) == bad_pos:
        return [vh]
    return [hv, vh]


def get_paths_from(code: str, start: Coords, keys: dict[str, Coords]) -> set[str]:
    permutations = set([""])
    current = start
    for key in code:
        paths = get_path_permutations(current, keys[key] - current, keys)
        current = keys[key]

        buffer = set()
        for perm in permutations:
            for path in paths:
                buffer.add(perm + path)
        permutations = buffer
    return permutations


def get_paths(code: str, keys: dict[str, Coords]) -> set[str]:
    return get_paths_from(code, keys["A"], keys)


# legacy function for fist star
def get_shortest_path(moves: str, depth: int) -> str:
    if depth == 1:
        return min(get_paths(moves, DIRECTIONAL_KEYS), key=len)

    paths = get_paths(moves, DIRECTIONAL_KEYS)
    return min(map(lambda path: get_shortest_path(path, depth - 1), paths), key=len)


def get_spf_between(start: str, end: str) -> str:
    return min(get_paths_from(end, DIRECTIONAL_KEYS[start], DIRECTIONAL_KEYS), key=len)


lookup: dict[(str, str, int), int] = dict()


def get_spf_len_between_depth(start: str, end: str, depth: int) -> int:
    if (start, end, depth) in lookup:
        return lookup[(start, end, depth)]

    if depth == 1:
        res = len(get_spf_between(start, end))
        lookup[(start, end, depth)] = res
        return res

    spf_len = 0
    moves = get_spf_between(start, end)
    prev_key = "A"
    for key in moves:
        spf_len += get_spf_len_between_depth(prev_key, key, depth - 1)
        prev_key = key
    lookup[(start, end, depth)] = spf_len
    return spf_len


# not an exact solution
def get_spf_len(moves: str, depth: int) -> int:
    spf_len = 0
    prev_key = "A"
    for key in moves:
        spf_len += get_spf_len_between_depth(prev_key, key, depth)
        prev_key = key
    return spf_len


if __name__ == "__main__":
    inp_raw: [str]
    with open("./input.txt", "r") as file:
        inp_raw = file.readlines()
    codes = [line.strip() for line in inp_raw]
    res = 0
    for code in codes:
        paths = get_paths(code, NUMERIC_KEYS)
        print(paths)
        spf = min(map(lambda path: get_spf_len(path, 25), paths))
        print(spf)
        res += int(code[:-1]) * spf
    print(res)
