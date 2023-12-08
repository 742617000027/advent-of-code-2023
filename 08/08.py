import re
from itertools import cycle
from math import gcd
from typing import Dict, List, Tuple

import utils

type Instructions = List[int]
type Mappings = Dict[str: Tuple[str, str]]


def parse() -> Tuple[Instructions, Mappings]:
    instructions_raw, mappings_raw = utils.read().split('\n\n')
    instructions = [0 if c == 'L' else 1 for c in instructions_raw]
    mappings = {
        k: tuple(re.findall(r'\w+', v))
        for k, v in [
            line.split(' = ')
            for line in mappings_raw.split('\n')
        ]
    }
    return instructions, mappings


def navigate(instructions: Instructions, mappings: Mappings, nodes: List[str] = ['AAA']) -> int:
    return lcm([count_steps(instructions, mappings, node, ghost_mode=len(nodes) > 1) for node in nodes])


def count_steps(instructions: Instructions, mappings: Mappings, node: str, ghost_mode: bool = False) -> int:
    for step, direction in enumerate(cycle(instructions)):
        node = mappings[node][direction]
        if node == 'ZZZ' or (ghost_mode and node[-1] == 'Z'):
            return step + 1


def lcm(l: List[int]) -> int:
    ret = 1
    for n in l: ret = ret * n // gcd(ret, n)
    return ret


def main():
    instructions, mappings = parse()

    # Part 1
    print('Part 1:', navigate(instructions, mappings))

    # Part 2
    nodes = [node for node in mappings.keys() if node[-1] == 'A']
    print('Part 2:', navigate(instructions, mappings, nodes))


if __name__ == "__main__":
    timer = utils.Timer()

    timer.start()
    main()
    timer.stop()  # 11.95ms
