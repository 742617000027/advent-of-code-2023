from itertools import cycle, product
from typing import Iterator, List, Tuple, Union

import utils

type Platform = List[List[str]]
type Direction = Union['north', 'east', 'south', 'west']


def cycle_tilt(platform: Platform, num_cycles: int = 10 ** 9, cycles: int = 0) -> Platform:
    platform_hash = get_platform_hash(platform)
    history = {platform_hash: 0}

    for cycles in range(1, num_cycles + 1):
        platform = perform_full_cycle(platform)
        platform_hash = get_platform_hash(platform)
        if platform_hash in history: break
        history[platform_hash] = cycles

    if cycles < num_cycles:
        cycle_len = cycles - history[platform_hash]
        remaining_cycles = (num_cycles - cycles) % cycle_len
        platform = cycle_tilt(platform, num_cycles=remaining_cycles)

    return platform


def perform_full_cycle(platform: Platform) -> Platform:
    for direction in ['north', 'west', 'south', 'east']:
        platform = tilt(platform, direction)
    return platform


def tilt(platform: Platform, direction: Direction) -> Platform:
    I, J = len(platform), len(platform[0])
    is_ns_dir, is_ew_dir = direction in ['north', 'south'], direction in ['east', 'west']
    i_range, j_range, ni_ranges, nj_ranges, i_offset, j_offset = get_ranges(I, J, direction)

    for (i, ni_range), (j, nj_range) in product(zip(i_range, ni_ranges), zip(j_range, nj_ranges)):

        if platform[i][j] == 'O':

            for ni, nj in zip(ni_range, nj_range):

                if platform[ni][nj] in 'O#':
                    platform[i][j] = '.'
                    platform[ni + i_offset][nj + j_offset] = 'O'
                    break

                if ((is_ns_dir and (ni == (I - 1) * (direction == 'south'))) or
                        (is_ew_dir and nj == (J - 1) * (direction == 'east'))):
                    platform[i][j] = '.'
                    platform[ni][nj] = 'O'

    return platform


def get_ranges(I: int, J: int, direction: Direction) \
        -> Tuple[range, range, List[Iterator[int]], List[Iterator[int]], int, int]:
    i_range, j_range = (
        (range(1, I) if direction == 'north' else range(I - 2, -1, -1), range(0, J))
        if direction in ['north', 'south'] else
        (range(0, I), range(1, J) if direction == 'west' else range(J - 2, -1, -1))
    )

    ni_ranges, nj_ranges, i_offset, j_offset = (
        [range(i - 1, -1, -1) if direction == 'north' else range(i + 1, I) for i in i_range],
        [cycle([j]) for j in j_range],
        1 if direction == 'north' else -1,
        0
    ) if direction in ['north', 'south'] else (
        [cycle([i]) for i in i_range],
        [range(j - 1, -1, -1) if direction == 'west' else range(j + 1, J) for j in j_range],
        0,
        1 if direction == 'west' else -1
    )

    return i_range, j_range, ni_ranges, nj_ranges, i_offset, j_offset


def calc_north_load(platform: Platform) -> int:
    I, load = len(platform), 0
    for i in range(0, I):
        load += platform[i].count('O') * (I - i)
    return load


def get_platform_hash(platform: Platform) -> int:
    return hash(tuple([tuple(row) for row in platform]))


def main():
    platform = [[c for c in line] for line in utils.read_str_lines()]

    # Part 1
    tilted_platform = tilt(platform, direction='north')
    print('Part 1:', calc_north_load(tilted_platform))

    # Part 2
    platform = cycle_tilt(platform)
    print('Part 2:', calc_north_load(platform))


if __name__ == "__main__":
    timer = utils.Timer()

    timer.start()
    main()
    timer.stop()  # 1637.18ms
