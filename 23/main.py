#!/usr/bin/env python3


def parse_connections(connections: [[str]]) -> dict[str, set[str]]:
    result = dict()
    for connection in connections:
        left = connection[0]
        right = connection[1]

        if left not in result:
            result[left] = set([right])
        else:
            result[left].add(right)

        if right not in result:
            result[right] = set([left])
        else:
            result[right].add(left)
    return result


def count_triplets_with_t(connections: dict[str, set[str]]) -> int:
    result = 0
    traversed: set[str] = set()
    for key in connections.keys():
        if key[0] != "t":
            continue
        traversed.add(key)

        for second in connections[key]:
            if second in traversed:
                continue
            for third in connections[second]:
                if third in traversed:
                    continue
                if key in connections[third]:
                    result += 1
    # divide since all secondary permutations are doubled
    return result // 2


# the Bron-Kerbosch algorithm
def bron_kerbosch(
    graph: dict[str, set[str]], R: set[str], P: set[str], X: set[str]
) -> [set[str]]:
    if len(P) == 0 and len(X) == 0:
        return [R]

    result = []
    buffer = list(P)
    for vertex in buffer:
        neighbours = graph[vertex]
        result.extend(
            bron_kerbosch(graph, R | {vertex}, P & neighbours, X & neighbours)
        )
        P -= {vertex}
        X &= {vertex}
    return result


def find_max_clique(graph: dict[str, set[str]]) -> set[str]:
    return max(
        bron_kerbosch(connections, set([]), set(connections.keys()), set([])),
        key=len,
    )


def get_password(connections: dict[str, set[str]]) -> str:
    clique = sorted(list(find_max_clique(connections)))
    return ",".join(clique)


if __name__ == "__main__":
    inp_raw: [str]
    with open("input.txt", "r") as file:
        inp_raw = file.readlines()
    conn_raw = [line.strip().split("-") for line in inp_raw]
    connections = parse_connections(conn_raw)
    print(count_triplets_with_t(connections))
    print(get_password(connections))
