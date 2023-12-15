from typing import Dict, List, Tuple

import utils

type Box = List[str]


def init(strings: List[str]) -> Tuple[List[Box], Dict[str, int]]:
    boxes, focals = [[] for _ in range(256)], dict()

    for string in strings:
        idx = string.find('=') if '=' in string else string.find('-')
        label = string[:idx]
        box = HASH(label)

        if '=' in string:
            focals[label] = int(string[idx + 1:])
            if label not in boxes[box]: boxes[box].append(label)

        if '-' in string and label in boxes[box]: boxes[box].pop(boxes[box].index(label))

    return boxes, focals


def HASH(string: str, val: int = 0) -> int:
    for c in string: val = ((val + ord(c)) * 17) % 256
    return val


def calc_focusing_power(boxes: List[Box], focals: Dict[str, int], total: int = 0) -> int:
    for b, box in enumerate(boxes, start=1):
        for l, label in enumerate(box, start=1):
            total += b * l * focals[label]
    return total


def main():
    strings = [s for s in utils.read().split(',')]

    # Part 1
    print('Part 1:', sum([HASH(string) for string in strings]))

    # Part 2
    boxes, focals = init(strings)
    print('Part 2:', calc_focusing_power(boxes, focals))


if __name__ == "__main__":
    timer = utils.Timer()

    timer.start()
    main()
    timer.stop()  # 6.23ms
