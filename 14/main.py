#!/bin/python3

import re
import math


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

    def distance(self, other: "Coords") -> int:
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, other: "Coords") -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: "Coords") -> bool:
        return self.x != other.x or self.y != other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class Robot:
    position: Coords
    velocity: Coords

    def __init__(self, pos_x: int, pos_y: int, vel_x: int, vel_y: int):
        self.position = Coords(pos_x, pos_y)
        self.velocity = Coords(vel_x, vel_y)

    def __repr__(self):
        return f"<Robot- Position: {self.position}, Velocity: {self.velocity}>"


def parse_input(inp: [int]) -> [Robot]:
    result = []
    while len(inp) > 3:
        result.append(Robot(inp.pop(0), inp.pop(0), inp.pop(0), inp.pop(0)))
    return result


MAP_DIMENSIONS = Coords(101, 103)
# MAP_DIMENSIONS = Coords(11, 7)

QUAD_WIDTH = math.floor(MAP_DIMENSIONS.x / 2)
QUAD_HEIGHT = math.floor(MAP_DIMENSIONS.y / 2)


def get_safety_factor(robots: [Robot]) -> int:
    for robot in robots:
        robot.position = (robot.position + 100 * robot.velocity) % MAP_DIMENSIONS

    quadrants = [0, 0, 0, 0]
    for robot in robots:
        pos = robot.position

        if pos.x > QUAD_WIDTH and pos.y < QUAD_HEIGHT:
            quadrants[0] += 1
        elif pos.x < QUAD_WIDTH and pos.y < QUAD_HEIGHT:
            quadrants[1] += 1
        elif pos.x < QUAD_WIDTH and pos.y > QUAD_HEIGHT:
            quadrants[2] += 1
        elif pos.x > QUAD_WIDTH and pos.y > QUAD_HEIGHT:
            quadrants[3] += 1

    print(quadrants)
    res = 1
    for quad in quadrants:
        res *= quad
    return res


def print_field(robots: [Robot]) -> None:
    field = [[" " for x in range(MAP_DIMENSIONS.x)] for y in range(MAP_DIMENSIONS.y)]

    for robot in robots:
        field[robot.position.y][robot.position.x] = "#"

    for row in field:
        print(*row)
    print()


def get_center_of_gravity(robots: [Robot]) -> Coords:
    center = Coords(0, 0)
    for robot in robots:
        center += robot.position

    center.x /= len(robots)
    center.y /= len(robots)
    return center


# esentially used to test how grouped the robots are
def get_avg_distances(robots: [Robot], center: Coords) -> int:
    distances = 0
    for robot in robots:
        distances += robot.position.distance(center)

    return distances / len(robots)


def find_christmas_tree(robots: [Robot]) -> int:
    offset = 5000
    for robot in robots:
        robot.position = (robot.position + offset * robot.velocity) % MAP_DIMENSIONS
    for i in range(1, 5000):
        for robot in robots:
            robot.position = (robot.position + robot.velocity) % MAP_DIMENSIONS
        center = get_center_of_gravity(robots)
        avg_dist = get_avg_distances(robots, center)
        if avg_dist < 33:
            print(f"{offset + i}, center: {center}, avg dist: {avg_dist}")
            print_field(robots)


if __name__ == "__main__":
    inpRaw: [str]
    with open("./input.txt", "r") as file:
        inpRaw = file.readlines()
    inp = re.findall(r"-?\d+", str(inpRaw))
    inp = list(map(int, inp))
    robots = parse_input(inp)
    # print(get_safety_factor(robots))
    find_christmas_tree(robots)
