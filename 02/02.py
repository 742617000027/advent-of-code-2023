import re
from functools import reduce
from operator import mul

import utils

LIMITS = {'red': 12, 'green': 13, 'blue': 14}


def get_values(i, line):
    _, cubes_part = line.split(': ')
    quantities = re.findall(r'(\d+) (blue|green|red)', cubes_part)
    maxvals = {color: maxval(quantities, color) for color in LIMITS.keys()}
    return i + 1 if possible(maxvals) else 0, power(maxvals)


def possible(maxvals):
    return all([maxvals[color] <= limit for color, limit in LIMITS.items()])


def power(maxvals):
    return reduce(mul, maxvals.values(), 1)


def maxval(quantities, color):
    return max([int(v) for v, c in quantities if c == color])


def main():
    games = utils.read_str_lines()
    ids, powers = utils.transpose([get_values(i, line) for i, line in enumerate(games)])

    # Part 1
    print(sum(ids))

    # Part 2
    print(sum(powers))


if __name__ == "__main__":
    timer = utils.Timer()

    timer.start()
    main()
    timer.stop()  # 1.47ms
