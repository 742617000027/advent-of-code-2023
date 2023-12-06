import re
from collections import deque
from typing import List, Tuple, Union

import utils

type Range = Tuple[int, int]
type Mapping = Tuple[int, int, int]


def parse(puzzle: str) -> Tuple[List[int], List[List[Mapping]]]:
    seed_str, *mappings_str = puzzle.split('\n\n')
    return get_seeds(seed_str), get_mappings(mappings_str)


def get_seeds(seed_str: str) -> List[int]:
    return [int(seed) for seed in utils.find_nums(seed_str)]


def get_mappings(mappings_str: str) -> List[List[Mapping]]:
    return [extract_mappings(mapping_str) for mapping_str in mappings_str]


def extract_mappings(mapping_str: str) -> List[Mapping]:
    _, *mapping_lines = mapping_str.split('\n')
    return [tuple([int(n) for n in utils.find_nums(mapping_line)]) for mapping_line in mapping_lines]


def get_locations_ranges(seeds: List[int], mappings: List[List[Mapping]]) -> List[Range]:
    ranges = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]
    for m in mappings:
        ranges = convert(ranges, m)
    return ranges


def convert(ranges: List[Range], mapping: List[Mapping]) -> List[Range]:
    ret: List[Range] = []
    queue = deque(ranges)

    while len(queue):
        range_to_map = queue.popleft()
        mapped_range, unmapped_range = map_range(range_to_map, mapping)
        ret.append(mapped_range)
        if unmapped_range: queue.append(unmapped_range)

    return ret


def map_range(range_to_map: Range, mapping: Mapping) -> Tuple[Range, Union[Range, None]]:
    range_start, range_len = range_to_map
    range_end = range_start + range_len

    for mapping_dest, mapping_source, mapping_range in mapping:

        start_in_range = in_range(range_start, mapping_source, mapping_range)
        end_in_range = in_range(range_end - 1, mapping_source, mapping_range)

        if start_in_range and end_in_range:
            return (mapping_dest + range_start - mapping_source, range_len), None

        if start_in_range:
            return ((mapping_dest + range_start - mapping_source, mapping_source + mapping_range - range_start),
                    (mapping_source + mapping_range, range_end - mapping_source - mapping_range))

        if end_in_range:
            return (mapping_dest, range_end - mapping_source), (range_start, mapping_source - range_start)

    return (range_start, range_len), None


def get_minimum(ranges: List[Range]) -> int:
    return min([s for s, _ in ranges])


def in_range(n: int, s: int, r: int) -> bool:
    return s <= n < s + r


def main():
    seeds, mappings = parse(utils.read())

    # Part 1
    location_ranges = get_locations_ranges([
        seeds[i // 2] if i % 2 == 0 else 1
        for i in range(len(seeds) * 2)
    ], mappings)
    print('Part 1:', get_minimum(location_ranges))

    # Part 2
    location_ranges = get_locations_ranges(seeds, mappings)
    print('Part 2:', get_minimum(location_ranges))


if __name__ == "__main__":
    timer = utils.Timer()

    timer.start()
    main()
    timer.stop()  # 2.55ms
