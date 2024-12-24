#!/bin/python3

MASK = 0xFFFFFF


def get_secret_number(secret: int) -> int:
    first = ((secret << 6) ^ secret) & MASK
    second = ((first >> 5) ^ first) & MASK
    third = ((second << 11) ^ second) & MASK
    return third


def get_nth_secret(secret: int, n: int) -> int:
    res = secret
    for i in range(n):
        res = get_secret_number(res)
    return res


seq_lookup: dict[(int, int, int, int), int] = dict()


def mark_sequences(secret: int, n: int) -> None:
    traversed: set[(int, int, int, int)] = set()
    prices = [secret % 10]
    changes = []
    for i in range(n):
        secret = get_secret_number(secret)
        changes.append(secret % 10 - prices[-1])
        prices.append(secret % 10)

        if i < 4:
            continue

        seq = (changes[-4], changes[-3], changes[-2], changes[-1])
        if seq in traversed:
            continue
        traversed.add(seq)

        if seq not in seq_lookup:
            seq_lookup[seq] = prices[-1]
        else:
            seq_lookup[seq] += prices[-1]


def most_optimal_sequence(secrets: [int], n: int) -> int:
    for secret in secrets:
        mark_sequences(secret, n)

    max_key = max(seq_lookup, key=seq_lookup.get)
    return seq_lookup[max_key]


if __name__ == "__main__":
    inp_raw: [str]
    with open("./input.txt", "r") as file:
        inp_raw = file.readlines()
    secrets = [int(line) for line in inp_raw]
    # print(sum(map(lambda s: get_nth_secret(s, 2000), secrets)))
    print(most_optimal_sequence(secrets, 2000))
