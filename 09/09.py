from typing import List, Tuple, Union

import utils


def extrapolate(report: List[int]) -> Tuple[int, int]:
    front, back = report[:1], report[-1]
    while len(set(report)) > 1:
        report = diff(report)
        front.append(report[0])
        back += report[-1]
    return reduce(front[::-1]), back


def diff(l: List[int]) -> List[int]:
    return [
        l[i + 1] - l[i]
        for i in range(len(l) - 1)
    ]


def reduce(l: List[int]) -> Union[int, List[int]]:
    if len(l) == 1: return l.pop()
    a, b, *r = l
    return reduce([b - a] + r)


def main():
    reports = [utils.find_nums(line) for line in utils.read_str_lines()]
    front, back = utils.transpose([extrapolate(report) for report in reports])

    # Part 1
    print('Part 1:', sum(back))

    # Part 2
    print('Part 2:', sum(front))


if __name__ == "__main__":
    timer = utils.Timer()

    timer.start()
    main()
    timer.stop()  # 4.21ms
