from collections import Counter, defaultdict, deque
from copy import deepcopy
from functools import cmp_to_key, reduce
from itertools import combinations, permutations, product

from time import process_time

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
DIAGDIRS = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
DIRS3D = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]


class Timer:
    def __init__(self):
        self.tic = 0
        self.toc = 0
        self.dur = 0

    def start(self):
        self.tic = process_time()

    def stop(self):
        self.toc = process_time()
        self.dur = self.toc - self.tic
        print(f'finished in {1000 * self.dur:.2f}ms')


def read_int_lines(file: str = 'input') -> list[int]:
    with open(file, 'r') as fp:
        sequence = [int(n) for n in fp.read().splitlines()]
    return sequence


def read_int_sequence(file: str = 'input') -> list[int]:
    with open(file, 'r') as fp:
        sequence = [int(n) for n in fp.read().split(',')]
    return sequence


def read_str_lines(file: str = 'input') -> list[str]:
    with open(file, 'r') as fp:
        sequence = fp.read().splitlines()
    return sequence


def read(file: str = 'input') -> str:
    with open(file, 'r') as fp:
        content = fp.read()
    return content


# collections
Counter = Counter
defaultdict = defaultdict
deque = deque

# copy
deepcopy = deepcopy

# functools
cmp_to_key = cmp_to_key
reduce = reduce

# itertools
combinations = combinations
permutations = permutations
product = product
