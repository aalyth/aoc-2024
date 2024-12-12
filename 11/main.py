#!/bin/python3

lookup: dict[(int, int), int] = dict()


def stone_splits(n: int, depth: int) -> int:
    if (n, depth) in lookup:
        return lookup[(n, depth)]

    if depth == 0:
        return 1

    if n == 0:
        res = stone_splits(1, depth - 1)
        lookup[(n, depth)] = res
        return res

    numlen = len(str(n))
    if numlen % 2 == 0:
        strn = str(n)
        numlen = int(numlen / 2)
        a = int(strn[:numlen])
        b = int(strn[numlen:])
        return stone_splits(a, depth - 1) + stone_splits(b, depth - 1)

    res = stone_splits(n * 2024, depth - 1)
    lookup[(n, depth)] = res
    return res


if __name__ == "__main__":
    inp = [7725, 185, 2, 132869, 0, 1840437, 62, 26310]
    res = [stone_splits(n, 75) for n in inp]
    print(sum(res))
