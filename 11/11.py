from copy import deepcopy
from itertools import product
from typing import List, Set, Tuple

import utils

type Universe = List[List[int]]
type Galaxy = Tuple[int, int]


def parse() -> Tuple[Universe, Set[Galaxy]]:
    replace = {'.': 1, '#': -1}
    image = [[replace[c] for c in line] for line in utils.read_str_lines()]
    I, J = len(image), len(image[0])
    galaxies = {(i, j) for i, j in product(range(I), range(J)) if image[i][j] == -1}
    return image, galaxies


def expand_universe(universe: Universe, expansion_factor: int = 2) -> Universe:
    I, J = len(universe), len(universe[0])
    expanded_universe = deepcopy(universe)

    for i in range(I):
        if all([point > 0 for point in universe[i]]):
            for j in range(J):
                expanded_universe[i][j] *= expansion_factor if expanded_universe[i][j] == 1 else 1

    for j in range(J):
        if all([universe[i][j] > 0 for i in range(I)]):
            for i in range(I):
                expanded_universe[i][j] *= expansion_factor if expanded_universe[i][j] == 1 else 1

    return expanded_universe


def get_total_of_shortest_paths(universe: Universe, galaxies: Set[Galaxy]) -> int:
    visits = {galaxy: set() for galaxy in galaxies}
    total = 0
    for source, dest in product(galaxies, galaxies):
        if source == dest or dest in visits[source]: continue
        visits[source].add(dest)
        total += pairwise_shortest_path(universe, source, dest)
        visits[dest].add(source)
    return total


def pairwise_shortest_path(universe: Universe, source: Galaxy, dest: Galaxy) -> int:
    (source_i, source_j), (dest_i, dest_j) = source, dest
    row_j_start, row_j_end = min(source_j, dest_j) + 1, max(source_j, dest_j) + 1
    col_i_start, col_i_end = min(source_i, dest_i) + 1, max(source_i, dest_i) + 1
    return (sum([abs(universe[source_i][j]) for j in range(row_j_start, row_j_end)]) +
            sum([abs(universe[i][dest_j]) for i in range(col_i_start, col_i_end)]))


def main():
    image, galaxies = parse()

    # Part 1
    slightly_expanded_universe = expand_universe(image)
    print('Part 1:', get_total_of_shortest_paths(slightly_expanded_universe, galaxies))

    # Part 2
    extremely_expanded_universe = expand_universe(image, expansion_factor=10 ** 6)
    print('Part 2:', get_total_of_shortest_paths(extremely_expanded_universe, galaxies))


if __name__ == "__main__":
    timer = utils.Timer()

    timer.start()
    main()
    timer.stop()  # 1290.75ms
