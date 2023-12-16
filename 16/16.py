from collections import deque

import utils


def parse():
    return [[c for c in line] for line in utils.read_str_lines()]


def LAZER(contraption, start):
    I, J = len(contraption), len(contraption[0])
    energized = [[set() for _ in range(J)] for _ in range(I)]
    beams = deque([start])

    while len(beams):
        beam = beams.popleft()
        (i, j), (di, dj) = beam
        ni, nj = i + di, j + dj

        if (not (0 <= ni < I and 0 <= nj < J)) or beam in energized[ni][nj]: continue

        energized[ni][nj].add(((i, j), (di, dj)))

        if contraption[ni][nj] == '.':
            beams.append(((ni, nj), (di, dj)))
            continue

        if contraption[ni][nj] == '\\':
            beams.append(((ni, nj), (dj, di)))
            continue

        if contraption[ni][nj] == '/':
            beams.append(((ni, nj), (-dj, -di)))
            continue

        if contraption[ni][nj] in '|':
            if (di, dj) in {(0, 1), (0, -1)}:
                beams.append(((ni, nj), (dj, di)))
                beams.append(((ni, nj), (-dj, di)))
            else:
                beams.append(((ni, nj), (di, dj)))
            continue

        if contraption[ni][nj] == '-':
            if (di, dj) in {(1, 0), (-1, 0)}:
                beams.append(((ni, nj), (dj, di)))
                beams.append(((ni, nj), (dj, -di)))
            else:
                beams.append(((ni, nj), (di, dj)))
            continue

    return [[len(s) > 0 for s in row] for row in energized]


def get_all_start_positions(I, J):
    start_positions = set()

    for i in range(I):
        start_positions.add(((i, -1), (0, 1)))
        start_positions.add(((i, J), (0, -1)))

    for j in range(J):
        start_positions.add(((-1, j), (1, 0)))
        start_positions.add(((I, j), (-1, 0)))

    return start_positions


def get_total(energized):
    return sum([tile for row in energized for tile in row])


def main():
    contraption = parse()

    # Part 1
    energized = LAZER(contraption, start=((0, -1), (0, 1)))
    print('Part 1:', get_total(energized))

    # Part 2
    I, J = len(contraption), len(contraption[0])
    start_positions = get_all_start_positions(I, J)
    print('Part 2:', max([
        get_total(energized)
        for energized in [
            LAZER(contraption, start=start_pos)
            for start_pos in start_positions
        ]
    ]))


if __name__ == "__main__":
    timer = utils.Timer()

    timer.start()
    main()
    timer.stop()  # 4115.99ms
