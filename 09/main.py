#!/bin/python3


def fs_pop(fs: list[str, int]) -> int:
    while fs[-1] == ".":
        fs.pop()
    return fs.pop()


def fs_checksum(files: [int]) -> int:
    fs = []
    for i in range(len(files)):
        if i % 2 == 0:
            file_idx = int(i / 2)
            fs.extend([file_idx] * files[i])
        else:
            fs.extend(["."] * files[i])

    i = 0
    while i < len(fs):
        if fs[i] == ".":
            res = fs_pop(fs)
            if i < len(fs):
                fs[i] = res
            else:
                fs.append(res)
                break
        i += 1
    checksum = 0
    for i in range(len(fs)):
        checksum += i * fs[i]
    return checksum


def find_viable_chunk_idx(files: [int], desired_len: int, bottom_idx: int) -> int:
    for i in range(len(files) - 1, bottom_idx, -1):
        if files[i][1] <= desired_len and files[i][0] != ".":
            return i
    return -1


def fs_checksum_ext(files: [int]) -> int:
    # compacted fs
    fs: list[([int, str], int)] = []
    for i in range(len(files)):
        if files[i] == 0:
            continue
        if i % 2 == 0:
            file_idx = int(i / 2)
            fs.append((file_idx, files[i]))
        else:
            fs.append((".", files[i]))

    i = 0
    while i < len(fs):
        if fs[i][0] != ".":
            i += 1
            continue
        desired_len = fs[i][1]
        idx = find_viable_chunk_idx(fs, desired_len, i)
        if idx == -1:
            i += 1
            continue
        if fs[idx][1] < desired_len:
            swapped_fs = fs[idx]
            del fs[idx]
            del fs[i]
            fs.insert(i, (".", desired_len - swapped_fs[1]))
            fs.insert(idx, (".", swapped_fs[1]))
            fs.insert(i, swapped_fs)
        else:
            fs[i], fs[idx] = fs[idx], fs[i]
        i += 1

    fs_expanded = []
    for el in fs:
        fs_expanded.extend([el[0]] * el[1])

    checksum = 0
    for i in range(len(fs_expanded)):
        if fs_expanded[i] == ".":
            continue
        checksum += i * int(fs_expanded[i])
    return checksum


if __name__ == "__main__":
    inp: [str]
    with open("./input.txt", "r") as file:
        inp = file.readlines()
    inp = [int(digit) for digit in inp[0].strip()]
    # print(fs_checksum(inp))
    print(fs_checksum_ext(inp))
    print("hello")
