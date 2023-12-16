from collections import deque
from typing import List, Set, Tuple, Union

import utils

type Beam = Tuple[Tuple[int, int], Tuple[int, int]]
type Layout = List[List[Union[str, bool]]]

OP = {
    '.': lambda di, dj: [(di, dj)],
    '\\': lambda di, dj: [(dj, di)],
    '/': lambda di, dj: [(-dj, -di)],
    '|': lambda di, dj: [(dj, di), (-dj, di)] if (di, dj) in {(0, 1), (0, -1)} else [(di, dj)],
    '-': lambda di, dj: [(dj, di), (dj, -di)] if (di, dj) in {(1, 0), (-1, 0)} else [(di, dj)]
}


def parse() -> Layout:
    return [[c for c in line] for line in utils.read_str_lines()]


def LAZER(contraption: Layout, start: Beam) -> Layout:
    I, J = len(contraption), len(contraption[0])
    energized = [[set() for _ in range(J)] for _ in range(I)]
    beams = deque([start])

    while len(beams):
        beam = beams.popleft()
        (i, j), (di, dj) = beam
        ni, nj = i + di, j + dj

        if (not (0 <= ni < I and 0 <= nj < J)) or beam in energized[ni][nj]: continue

        energized[ni][nj].add(beam)
        tile = contraption[ni][nj]
        beams.extend([((ni, nj), (ndi, ndj)) for ndi, ndj in OP[tile](di, dj)])

    return [[len(s) > 0 for s in row] for row in energized]


def get_all_start_positions(I: int, J: int) -> Set[Beam]:
    start_positions = set()

    for i in range(I):
        start_positions.add(((i, -1), (0, 1)))
        start_positions.add(((i, J), (0, -1)))

    for j in range(J):
        start_positions.add(((-1, j), (1, 0)))
        start_positions.add(((I, j), (-1, 0)))

    return start_positions


def get_total(energized: Layout) -> int:
    return sum([tile for row in energized for tile in row])


def main():
    contraption = parse()

    # Part 1
    energized = LAZER(contraption, start=((0, -1), (0, 1)))
    print('Part 1:', get_total(energized))

    # Part 2
    I, J = len(contraption), len(contraption[0])
    start_positions = get_all_start_positions(I, J)
    print('Part 2:', max([
        get_total(energized)
        for energized in [
            LAZER(contraption, start=start_pos)
            for start_pos in start_positions
        ]
    ]))


if __name__ == "__main__":
    timer = utils.Timer()

    timer.start()
    main()
    timer.stop()  # 4115.99ms
