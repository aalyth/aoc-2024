#!/bin/python3


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

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, other: "Coords") -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: "Coords") -> bool:
        return self.x != other.x or self.y != other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class Map:
    field: [[str]]
    moves: [str]

    def __init__(self, field: [[str]], moves: [str]) -> None:
        self.field = field
        self.moves = moves

    def __getitem__(self, idx: Coords) -> str:
        if not self.valid_coords(idx):
            raise IndexError(f"invalid indexing of Map: {idx}")
        return self.field[idx.y][idx.x]

    def __setitem__(self, idx: Coords, val: str) -> str:
        if not self.valid_coords(idx):
            raise IndexError(f"invalid indexing of Map: {idx}")
        self.field[idx.y][idx.x] = val
        return val

    def __repr__(self) -> str:
        result = ""
        for row in self.field:
            result += "".join(row)
            result += "\n"
        return result

    def expand(self) -> None:
        new_field = []
        for row in self.field:
            tmp = []
            for ch in row:
                match ch:
                    case "@":
                        tmp.append("@")
                        tmp.append(".")
                    case "#":
                        tmp.append("#")
                        tmp.append("#")
                    case "O":
                        tmp.append("[")
                        tmp.append("]")
                    case ".":
                        tmp.append(".")
                        tmp.append(".")
            new_field.append(tmp)
        self.field = new_field

    def valid_coords(self, idx: Coords) -> bool:
        return (
            idx.x >= 0
            or idx.x < len(self.field[0])
            or idx.y >= 0
            or idx.y < len(self.field)
        )


def split_input(inp: [str]) -> ([str], [str]):
    return (first_half, second_half)


def parse_input(inp: [str]) -> Map:
    split_idx = 0
    for i in range(len(inp)):
        if inp[i] == "\n":
            split_idx = i
            break
    first_half = inp[:split_idx]
    second_half = inp[split_idx + 1 :]

    field = [list(line.strip()) for line in first_half]
    moves = [move for line in second_half for move in line.strip()]
    return Map(field, moves)


def get_submarine_coords(_map: Map) -> Coords:
    for y in range(len(_map.field)):
        for x in range(len(_map.field[0])):
            idx = Coords(x, y)
            if _map[idx] == "@":
                return idx
    raise ValueError()


def move_to_direction(move: str) -> Coords:
    match move:
        case "^":
            return Coords(0, -1)
        case "v":
            return Coords(0, 1)
        case "<":
            return Coords(-1, 0)
        case ">":
            return Coords(1, 0)
    raise ValueError("invalid movement")


def is_crate_blocked(_map: Map, pos: Coords, direction: Coords) -> bool:
    if direction != Coords(0, 1) and direction != Coords(0, -1):
        raise ValueError("`is_crate_blocked()` must be used only for vertical checking")

    next_pos = pos + direction
    match _map[pos]:
        case "#":
            return True
        case ".":
            return False
        case "[":
            return is_crate_blocked(_map, next_pos, direction) or is_crate_blocked(
                _map, next_pos + Coords(1, 0), direction
            )
        case "]":
            return is_crate_blocked(_map, next_pos, direction) or is_crate_blocked(
                _map, next_pos + Coords(-1, 0), direction
            )
    return True


def move_crates(_map: Map, pos: Coords, direction: Coords):
    if direction != Coords(0, 1) and direction != Coords(0, -1):
        raise ValueError("`is_crate_blocked()` must be used only for vertical checking")

    if _map[pos] != "[" and _map[pos] != "]":
        return

    second_pos: Coords
    if _map[pos] == "[":
        second_pos = pos + Coords(1, 0)
    else:
        second_pos = pos + Coords(-1, 0)

    next_pos = pos + direction
    sec_next_pos = second_pos + direction

    if _map[next_pos] != "." or _map[sec_next_pos] != ".":
        move_crates(_map, next_pos, direction)
        move_crates(_map, sec_next_pos, direction)

    _map[pos], _map[next_pos] = _map[next_pos], _map[pos]
    _map[second_pos], _map[sec_next_pos] = _map[sec_next_pos], _map[second_pos]


# returns whether the object was actually moved - used to check the submarine
# movement
def move_obstacles(_map: Map, pos: Coords, direction: Coords) -> bool:
    next_pos = pos + direction
    match _map[next_pos]:
        case "#":
            return
        case ".":
            _map[next_pos] = _map[pos]
            _map[pos] = "."
            return True
        case "O":
            move_obstacles(_map, next_pos, direction)
            if _map[next_pos] == ".":
                _map[next_pos] = _map[pos]
                _map[pos] = "."
                return True
        case "[" | "]":
            if direction == Coords(1, 0) or direction == Coords(-1, 0):
                move_obstacles(_map, next_pos, direction)
                if _map[next_pos] == ".":
                    _map[next_pos] = _map[pos]
                    _map[pos] = "."
                    return True
            elif is_crate_blocked(_map, next_pos, direction):
                return False
            else:
                move_crates(_map, next_pos, direction)
                _map[next_pos], _map[pos] = _map[pos], _map[next_pos]
                return True

    return False


def get_gps_coordinates(_map: Map) -> int:
    submarine = get_submarine_coords(_map)

    for move in _map.moves:
        direction = move_to_direction(move)
        if move_obstacles(_map, submarine, direction):
            submarine += direction

    result = 0
    for y in range(len(_map.field)):
        for x in range(len(_map.field[0])):
            if _map.field[y][x] == "O" or _map.field[y][x] == "[":
                result += y * 100 + x

    return result


if __name__ == "__main__":
    inp_raw: [str]
    with open("./input.txt", "r") as file:
        inp_raw = file.readlines()
    _map = parse_input(inp_raw)
    _map.expand()
    print(_map)
    print(get_gps_coordinates(_map))
