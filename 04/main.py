#!/bin/env python3


def valid_xmas(inp: [str], ln: int, col: int, ln_dir: int, col_dir: int) -> bool:
    for ch in "XMAS":
        if ln < 0 or ln >= len(inp) or col < 0 or col >= len(inp[0]):
            return False
        if inp[ln][col] != ch:
            return False
        ln += ln_dir
        col += col_dir

    return True


def check_xmas(inp: [str], ln: int, col: int) -> int:
    return sum(
        [
            valid_xmas(inp, ln, col, 1, 0),
            valid_xmas(inp, ln, col, 0, 1),
            valid_xmas(inp, ln, col, -1, 0),
            valid_xmas(inp, ln, col, 0, -1),
            valid_xmas(inp, ln, col, 1, 1),
            valid_xmas(inp, ln, col, -1, -1),
            valid_xmas(inp, ln, col, -1, 1),
            valid_xmas(inp, ln, col, 1, -1),
        ]
    )


def get_xmas_occurances(inp: [str]) -> int:
    lines = len(inp)
    line_len = len(inp[0])

    xmas_count = 0
    for i in range(lines):
        for j in range(line_len):
            if inp[i][j] != "X":
                continue

            xmas_count += check_xmas(inp, i, j)
    return xmas_count


def check_x_mas(inp: [str], ln: int, col: int) -> int:
    if ln <= 0 or col <= 0 or ln + 1 >= len(inp) or col + 1 >= len(inp[0]):
        return 0
    return sum(
        [
            (
                inp[ln - 1][col - 1] == "M"
                and inp[ln + 1][col - 1] == "M"
                and inp[ln - 1][col + 1] == "S"
                and inp[ln + 1][col + 1] == "S"
            ),
            (
                inp[ln - 1][col + 1] == "M"
                and inp[ln + 1][col + 1] == "M"
                and inp[ln - 1][col - 1] == "S"
                and inp[ln + 1][col - 1] == "S"
            ),
            (
                inp[ln - 1][col - 1] == "M"
                and inp[ln - 1][col + 1] == "M"
                and inp[ln + 1][col - 1] == "S"
                and inp[ln + 1][col + 1] == "S"
            ),
            (
                inp[ln + 1][col - 1] == "M"
                and inp[ln + 1][col + 1] == "M"
                and inp[ln - 1][col - 1] == "S"
                and inp[ln - 1][col + 1] == "S"
            ),
        ]
    )


def get_x_mas_occurances(inp: [str]) -> int:
    lines = len(inp)
    line_len = len(inp[0])

    xmas_count = 0
    for i in range(lines):
        for j in range(line_len):
            if inp[i][j] != "A":
                continue

            xmas_count += check_x_mas(inp, i, j)
    return xmas_count


if __name__ == "__main__":
    inp: [str]
    with open("./input.txt", "r") as file:
        inp = file.readlines()
    inp = [line.strip() for line in inp]
    print(get_xmas_occurances(inp))
    print(get_x_mas_occurances(inp))
