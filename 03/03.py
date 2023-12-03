import re
from typing import List, Set, Tuple

import utils

type Number = Tuple[str, Tuple[int, int]]


def get_all_numbers(rows: List[str]) -> List[Tuple[Number, int]]:
    return [(number, r) for r, row in enumerate(rows) for number in get_in_row(r'\d+', row)]


def get_unique_symbols(engine: str) -> Set[str]:
    return set(re.findall(r'[^\d.\\n]', engine))


def get_valid_numbers(rows: List[str], numbers: List[Tuple[Number, int]], symbols: Set[str]) -> List[int]:
    len_line = len(rows[0])
    return [
        int(n)
        for ((n, number_pos), number_r) in numbers
        if is_symbol_adjacent(number_r, number_pos, rows, len_line, symbols)
    ]


def is_symbol_adjacent(number_r: int, number_pos: Tuple[int, int], rows: List[str],
                       len_line: int, symbols: Set[str]) -> bool:
    start, end = number_pos
    row_prev, row_next = max(number_r - 1, 0), min(number_r + 1, len(rows) - 1)
    search_start, search_end = max(start - 1, 0), min(end + 1, len_line)
    for sym in symbols:
        if any([
            sym in rows[row_prev][search_start:search_end],
            sym in rows[number_r][search_start:search_end],
            sym in rows[row_next][search_start:search_end]
        ]):
            return True
    return False


def get_gear_ratios(rows: List[str], numbers: List[Tuple[Number, int]]) -> List[int]:
    return [
        adjacent_numbers[0] * adjacent_numbers[1]
        for adjacent_numbers in [
            get_adjacent_numbers(r, gear_pos, numbers)
            for r, row in enumerate(rows)
            for (_, (gear_pos, _)) in get_in_row(r'\*', row)
        ]
        if is_gear(adjacent_numbers)
    ]


def get_adjacent_numbers(gear_r: int, gear_pos: int, numbers: List[Number]) -> List[int]:
    return [
        int(n)
        for ((n, (number_start, number_end)), number_r) in numbers
        if (gear_r - 1 <= number_r <= gear_r + 1) and (number_start - 1 <= gear_pos <= number_end)
    ]


def is_gear(adjacent_numbers: List[int]) -> bool:
    return len(adjacent_numbers) == 2


def get_in_row(pattern: str, row: str) -> List[Tuple[str, Tuple[int, int]]]:
    return [(m.group(), (m.start(), m.end())) for m in re.finditer(pattern, row)]


def main():
    engine = utils.read()
    rows = engine.split('\n')
    numbers = get_all_numbers(rows)
    symbols = get_unique_symbols(engine)

    # Part 1
    valid_numbers = get_valid_numbers(rows, numbers, symbols)
    print('Part 1:', sum(valid_numbers))

    # Part 2
    gear_ratios = get_gear_ratios(rows, numbers)
    print('Part 2:', sum(gear_ratios))


if __name__ == "__main__":
    timer = utils.Timer()

    timer.start()
    main()
    timer.stop()  # 20.31ms
