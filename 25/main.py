#!/usr/bin/env python3

import numpy as np


# returns the locks and keys
def parse_input(inp: [str]) -> ([[int]], [[int]]):
    parsed = []
    while True:
        try:
            split_idx = inp.index("")
            buff = np.transpose([list(line) for line in inp[:split_idx]]).tolist()
            parsed.append(buff)
            inp = inp[split_idx + 1 :]
        except ValueError:
            parsed.append(np.transpose([list(line) for line in inp]).tolist())
            break

    locks = []
    keys = []
    for block in parsed:
        if block[0][0] == ".":
            key = []
            for row in block:
                key.append(row.count("#") - 1)
            keys.append(key)
        else:
            lock = []
            for row in block:
                lock.append(row.count("#") - 1)
            locks.append(lock)

    return locks, keys


def count_non_overlapping(keys: [[int]], locks: [[int]]):
    result = 0
    for lock in locks:
        for key in keys:
            is_valid = True
            for l, k in zip(lock, key):
                if l + k >= 6:
                    is_valid = False
                    break
            result += is_valid
    return result


if __name__ == "__main__":
    inp_raw: [str]
    with open("./input.txt", "r") as file:
        inp_raw = file.readlines()
    inp_raw = [line.strip() for line in inp_raw]
    locks, keys = parse_input(inp_raw)
    print(count_non_overlapping(keys, locks))
