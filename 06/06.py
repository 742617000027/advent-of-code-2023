from math import ceil, floor
from typing import List, Tuple

import utils

type Race = Tuple[int, int]
type Bound = Tuple[int, int]


def get_races(puzzle: List[str]) -> List[Race]:
    return list(zip(*[[int(n) for n in utils.find_nums(line)] for line in puzzle]))


def get_single_race(puzzle: List[str]) -> Race:
    return tuple(int(''.join(utils.find_nums(line))) for line in puzzle)


def get_bounds(time: int, record: int) -> Bound:
    return (floor((0.5 * (time - (time ** 2 - 4 * record) ** 0.5))) + 1,
            ceil((0.5 * ((time ** 2 - 4 * record) ** 0.5 + time)) - 1))


def count(lower: int, upper: int) -> int:
    return upper - lower + 1


def prod(vals: List[int], ret: int = 1) -> int:
    for v in vals: ret *= v
    return ret


def main():
    puzzle = utils.read_str_lines()

    # Part 1
    races = get_races(puzzle)
    bounds = [get_bounds(*race) for race in races]
    n_ways_to_win = [count(*bound) for bound in bounds]
    print('Part 1:', prod(n_ways_to_win))

    # Part 2
    race = get_single_race(puzzle)
    bound = get_bounds(*race)
    print('Part 2:', count(*bound))


if __name__ == "__main__":
    timer = utils.Timer()

    timer.start()
    main()
    timer.stop()  # 0.29ms
