import re
from typing import List

import utils


def get_all_numbers(rows):
    return [(number, r) for r, row in enumerate(rows) for number in get_in_row(r'\d+', row)]


def get_unique_symbols(engine):
    return set(re.findall(r'[^\d.\\n]', engine))


def get_valid_numbers(rows, numbers, symbols):
    len_line = len(rows[0])
    return [int(n) for ((n, pos), r) in numbers if is_symbol_adjacent(r, pos, rows, len_line, symbols)]


def get_gear_ratios(rows, numbers):
    return [
        adjacent_numbers[0] * adjacent_numbers[1]
        for adjacent_numbers in [
            numbers_adjacent(gear_pos, r, numbers)
            for r, row in enumerate(rows)
            for (_, (gear_pos, _)) in get_in_row(r'\*', row)
        ]
        if is_gear(adjacent_numbers)
    ]


def is_gear(adjacent_numbers):
    return len(adjacent_numbers) == 2


def numbers_adjacent(gear_pos, gear_r, numbers):
    return [
        int(n)
        for ((n, (number_start, number_end)), number_r) in numbers
        if (gear_r - 1 <= number_r <= gear_r + 1) and (number_start - 1 <= gear_pos <= number_end)
    ]


def is_symbol_adjacent(r, pos, rows: List[str], len_line, symbols):
    start, end = pos
    row_prev, row_next = max(r - 1, 0), min(r + 1, len(rows) - 1)
    search_start, search_end = max(start - 1, 0), min(end + 1, len_line)
    for sym in symbols:
        if any([
            sym in rows[row_prev][search_start:search_end],
            sym in rows[r][search_start:search_end],
            sym in rows[row_next][search_start:search_end]
        ]):
            return True
    return False


def get_in_row(pattern, row):
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
    timer.stop()  # 39.80ms
