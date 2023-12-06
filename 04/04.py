import re
from typing import List, Set, Tuple

import utils

type Card = Tuple[Set[int], Set[int]]


def get_cards(puzzle: List[str]) -> List[Card]:
    return [get_card(line) for line in puzzle]


def get_card(line: str) -> Card:
    return tuple([string_to_nums(string) for string in line.split(': ').pop().split(' | ')])


def string_to_nums(string: str) -> Set[int]:
    return set(utils.find_nums(string))


def get_points(winning: Set[int], my: Set[int]) -> int:
    num_hits = len(winning.intersection(my))
    return 2 ** (num_hits - 1) if num_hits else 0


def play(cards: List[Card]) -> int:
    num_copies = {i: 1 for i in range(len(cards))}
    for i, (winning, my) in enumerate(cards):
        num_hits = len(winning.intersection(my))
        for j in range(i + 1, i + num_hits + 1):
            num_copies[j] += num_copies[i]
    return sum(num_copies.values())


def main():
    cards = get_cards(utils.read_str_lines())

    # Part 1
    points = [get_points(*card) for card in cards]
    print('Part 1:', sum(points))

    # Part 2
    print('Part 2:', play(cards))


if __name__ == "__main__":
    timer = utils.Timer()

    timer.start()
    main()
    timer.stop()  # 2.55ms
