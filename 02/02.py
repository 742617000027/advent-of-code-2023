import re
from collections import defaultdict
from functools import reduce
from operator import mul

import utils

LIMITS = {'red': 12, 'green': 13, 'blue': 14}


def get_values(line):
    game_part, cubes_part = line.split(': ')
    game_id = int(game_part.replace('Game ', ''))
    quantities = re.findall('(\d+) (blue|green|red)', cubes_part)
    return game_id if all([int(v) <= LIMITS[color] for v, color in quantities]) else 0, \
        prod(minimums(quantities).values())


def minimums(quantities):
    d = defaultdict(int)
    for v, color in quantities:
        if int(v) > d[color]: d[color] = int(v)
    return d


def prod(l):
    return reduce(mul, l, 1)


if __name__ == "__main__":
    timer = utils.Timer()

    # Part 1
    # timer.start()
    # games = utils.read_str_lines()
    # ids, _ = list(zip(*[get_values(line) for line in games]))
    # print(sum(ids))
    # timer.stop()  # 4.12ms

    # Part 2
    timer.start()
    games = utils.read_str_lines()
    _, powers = list(zip(*[get_values(line) for line in games]))
    print(sum(powers))
    timer.stop()  # 4.22ms
