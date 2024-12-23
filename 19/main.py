#!/bin/python3


class Trie:
    is_terminal: bool
    children: dict[str, "Trie"]

    def __init__(self) -> None:
        self.children = dict()
        self.is_terminal = False

    def add_pattern(self, pattern: str) -> None:
        node = self
        for ch in pattern:
            if ch not in node.children:
                node.children[ch] = Trie()
            node = node.children[ch]
        node.is_terminal = True

    def get_patterns(self, design: str) -> [str]:
        buffer = ""
        result = []
        node = self
        for ch in design:
            buffer += ch
            if ch not in node.children:
                break
            node = node.children[ch]
            if node.is_terminal:
                result.append(buffer)
        return result

    def __repr__(self) -> str:
        if not self.children:
            return f"<{self.is_terminal}>"
        return f"({self.children}, <{self.is_terminal}>)"


is_valid_lookup: dict[str, bool] = dict()


def is_valid(design: str, tree: Trie) -> bool:
    if design in is_valid_lookup:
        return is_valid_lookup[design]

    if design == "":
        return True

    patterns = tree.get_patterns(design)
    for pattern in patterns:
        if is_valid(design[len(pattern) :], tree):
            is_valid_lookup[design] = True
            return True

    is_valid_lookup[design] = False
    return False


valid_patterns_lookup: dict[str, int] = dict()


def count_valid_patterns(design: str, tree: Trie) -> bool:
    if design in valid_patterns_lookup:
        return valid_patterns_lookup[design]

    if design == "":
        return 1

    valid_patterns = 0
    patterns = tree.get_patterns(design)
    for pattern in patterns:
        valid_patterns += count_valid_patterns(design[len(pattern) :], tree)
    valid_patterns_lookup[design] = valid_patterns
    return valid_patterns


if __name__ == "__main__":
    inp_raw: [str]
    with open("./input.txt", "r") as file:
        inp_raw = file.readlines()
    patterns = inp_raw[0].strip().split(", ")

    tree = Trie()
    for pattern in patterns:
        tree.add_pattern(pattern)

    designs = [line.strip() for line in inp_raw[2:]]
    count = 0
    for design in designs:
        count += count_valid_patterns(design, tree)
    print(count)
