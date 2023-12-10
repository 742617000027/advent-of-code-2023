from collections import deque
from random import choice
from typing import Dict, List, Set, Tuple, Union

import utils
from utils import DIRS

type Scan = List[List[str]]
type Position = Tuple[int, int]
type Move = Tuple[int, int]

HERE, THERE, NOWHERE = '█', '░', ' '

# OUT stores legal moves that exit each tile and, depending on the direction in which the tile is exited,
# the relative neighbors that would be considered left and right respectively.
OUT: Dict[str, Dict[Move, Tuple[Set[Move], Set[Move]]]] = {
    '│': {
        (-1, 0): ({(0, -1)}, {(0, 1)}),
        (1, 0): ({(0, 1)}, {(0, -1)})
    },
    '─': {
        (0, 1): ({(-1, 0)}, {(1, 0)}),
        (0, -1): ({(1, 0)}, {(-1, 0)})
    },
    '└': {
        (-1, 0): ({(0, -1), (1, -1), (1, 0)}, set()),
        (0, 1): (set(), {(0, -1), (1, -1), (1, 0)})
    },
    '┘': {
        (-1, 0): (set(), {(1, 0), (1, 1), (0, 1)}),
        (0, -1): ({(1, 0), (1, 1), (0, 1)}, set())
    },
    '┐': {
        (0, -1): (set(), {(-1, 0), (-1, 1), (0, 1)}),
        (1, 0): ({(-1, 0), (-1, 1), (0, 1)}, set())
    },
    '┌': {
        (0, 1): ({(0, -1), (-1, -1), (-1, 0)}, set()),
        (1, 0): (set(), {(0, -1), (-1, -1), (-1, 0)})
    }
}


def parse() -> Tuple[Scan, Position]:
    translation = str.maketrans('|-LJ7F', ''.join([c for c in OUT.keys()]))
    scan = [
        [
            pipe
            for pipe in line
        ]
        for line in utils.read().translate(translation).split('\n')
    ]
    return scan, find_start(scan)


def find_start(scan: Scan) -> Position:
    for i, row in enumerate(scan):
        for j, tile in enumerate(row):
            if tile == 'S':
                return i, j


def walk(scan: Scan, start: Position) -> Tuple[int, Scan]:
    marked_scan: Scan = [[NOWHERE for _ in row] for row in scan]
    position = start
    start_tile, start_moves = find_start_tile_and_moves(scan, position)
    scan[start[0]][start[1]] = start_tile
    loop = {start}
    steps = 0

    while True:
        i, j = position
        move = find_next_move(scan, position, loop) \
            if len(loop) > 1 \
            else pick_random(start_moves)

        if not move:
            marked_scan = mark(scan, marked_scan, position, (start[0] - position[0], start[1] - position[1]))
            return steps + 1, marked_scan

        di, dj = move
        marked_scan = mark(scan, marked_scan, position, move)
        position = i + di, j + dj
        loop.add(position)
        steps += 1


def find_start_tile_and_moves(scan: Scan, start: Position) -> Tuple[str, Set[Move]]:
    entered_by = get_moves_and_the_tiles_they_enter()
    moves = set()
    i, j = start

    for di, dj in DIRS:
        ni, nj = i + di, j + dj

        if scan[ni][nj] in entered_by[(di, dj)]:
            moves.add((di, dj))

    tile = [tile for tile in OUT if all([move in OUT[tile] for move in moves])].pop()
    return tile, moves


def get_moves_and_the_tiles_they_enter():
    return {
        move: ''.join(
            k for k, moves_out in OUT.items()
            for move_out in moves_out
            if move == tuple(-x for x in move_out)
        )
        for move in DIRS
    }


def find_next_move(scan: Scan, position: Position, loop: Set[Position]) -> Union[Move, None]:
    all_moves = get_all_moves(scan, position)
    legal_moves = get_legal_moves(position, all_moves, loop)
    return legal_moves.pop() if len(legal_moves) > 0 else None


def get_all_moves(scan: Scan, position: Position) -> Set[Move]:
    return set(OUT[get_tile(scan, position)].keys())


def get_legal_moves(position: Position, moves: Set[Move], loop: Set[Position]) -> List[Move]:
    i, j = position
    return [(di, dj) for di, dj in moves if (i + di, j + dj) not in loop]


def pick_random(moves: Set[Move]) -> Move:
    return choice(list(moves))


def mark(scan: Scan, marked_scan: Scan, position: Position, move: Move) -> Scan:
    I, J = len(scan), len(scan[0])
    tile = get_tile(scan, position)
    left, right = OUT[tile][move]
    i, j = position
    marked_scan[i][j] = tile

    for side, marker in zip([left, right], [HERE, THERE]):

        for di, dj in side:
            ni, nj = i + di, j + dj

            if 0 <= ni < I and 0 <= nj < J and marked_scan[ni][nj] == NOWHERE:
                marked_scan[ni][nj] = marker

    return marked_scan


def count_enclosed(marked_scan: Scan):
    sides = {marker: find_marker_positions(marked_scan, marker) for marker in [HERE, THERE]}

    for side, positions in sides.items():

        for position in positions:
            marked_scan = floodfill(position, marked_scan)

    inner_maker = find_inner_marker(marked_scan)
    printable = '\n'.join([''.join(line) for line in marked_scan])

    return printable.count(inner_maker)


def find_marker_positions(marked_scan: Scan, side: str) -> Set[Position]:
    ret = set()
    for i in range(len(marked_scan)):
        for j in range(len(marked_scan[0])):
            if get_tile(marked_scan, (i, j)) == side:
                ret.add((i, j))

    return ret


def floodfill(position: Position, marked_scan: Scan) -> Scan:
    I, J = len(marked_scan), len(marked_scan[0])
    tile = get_tile(marked_scan, position)
    queue = deque([position])

    while queue:
        i, j = queue.popleft()
        for di, dj in DIRS:
            ni, nj = i + di, j + dj
            if 0 <= ni < I and 0 <= nj < J and marked_scan[ni][nj] == NOWHERE:
                marked_scan[ni][nj] = tile
                queue.append((ni, nj))

    return marked_scan


def find_inner_marker(marked_scan: Scan) -> str:
    I, J = len(marked_scan), len(marked_scan[0])
    sides = {HERE: THERE, THERE: HERE}

    for j in range(J):
        if marked_scan[0][j] in sides: return sides[marked_scan[0][j]]
        if marked_scan[I - 1][j] in sides: return sides[marked_scan[I - 1][j]]

    for i in range(1, I - 1):
        if marked_scan[i][0] in sides: return sides[marked_scan[i][0]]
        if marked_scan[i][J - 1] in sides: return sides[marked_scan[i][J - 1]]


def get_tile(scan: Scan, position: Position) -> str:
    i, j = position
    return scan[i][j]


def main():
    scan, start = parse()
    steps, marked_scan = walk(scan, start)

    # Part 1
    print('Part 1:', steps // 2)

    # Part 2
    print('Part 2:', count_enclosed(marked_scan))


if __name__ == "__main__":
    timer = utils.Timer()

    timer.start()
    main()
    timer.stop()  # 46.11ms
