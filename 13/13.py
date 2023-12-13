from typing import List

import numpy as np

import utils


def parse() -> List[np.ndarray]:
    replacer = {'.': 0, '#': 1}
    return [
        np.array([
            [replacer[c] for c in row]
            for row in pattern.split('\n')
        ], dtype=np.int8)
        for pattern in utils.read().split('\n\n')
    ]


def find_reflection_value(pattern: np.ndarray, smudged: bool = False) -> int:
    for axis in range(2):
        size = pattern.shape[axis]

        for d in range(1, size):
            window_size = min(d, size - d)
            a = pattern[:, d - window_size:d] if axis == 1 else pattern[d - window_size:d, :]
            b = pattern[:, d:d + window_size] if axis == 1 else pattern[d:d + window_size, :]
            diff = np.sum(np.abs(a - np.flip(b, axis)))
            if diff == +smudged: return d * (1 if axis else 100)


def main():
    puzzle = parse()

    # Part 1
    reflection_values = [find_reflection_value(pattern) for pattern in puzzle]
    print('Part 1:', sum(reflection_values))

    # Part 2
    smudged_reflection_values = [find_reflection_value(pattern, smudged=True) for p, pattern in enumerate(puzzle)]
    print('Part 2:', sum(smudged_reflection_values))


if __name__ == "__main__":
    timer = utils.Timer()

    timer.start()
    main()
    timer.stop()  # 99.83ms
