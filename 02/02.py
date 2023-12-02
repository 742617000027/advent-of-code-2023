import re
from functools import reduce
from operator import mul

import utils

LIMITS = {'red': 12, 'green': 13, 'blue': 14}


def get_values(i, line):
    _, cubes_part = line.split(': ')
    quantities = re.findall('(\d+) (blue|green|red)', cubes_part)
    return i + 1 if possible(quantities) else 0, power(quantities)


def possible(quantities):
    return all([int(v) <= LIMITS[color] for v, color in quantities])


def power(quantities):
    return prod([maxval(quantities, color) for color in LIMITS.keys()])


def maxval(quantities, color):
    return max([int(v) for v, c in quantities if c == color])


def prod(l):
    return reduce(mul, l, 1)


def main():
    games = utils.read_str_lines()
    ids, powers = list(zip(*[get_values(i, line) for i, line in enumerate(games)]))

    # Part 1
    print(sum(ids))

    # Part 2
    print(sum(powers))


if __name__ == "__main__":
    timer = utils.Timer()

    timer.start()
    main()
    timer.stop()  # 1.47ms
