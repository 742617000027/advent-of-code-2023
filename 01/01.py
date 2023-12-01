import utils

DIGITS_MAP = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}


def get_calibration_value(line, as_letters=False):
    stripped = [c for c in line if c in [str(d) for d in range(10)]]
    first_real_digit, last_real_digit = stripped[0], stripped[-1]

    if as_letters:

        first_real_digit_idx = line.find(first_real_digit)
        last_real_digit_idx = len(line) - line[::-1].find(last_real_digit) - 1

        for k, v in DIGITS_MAP.items():
            idx = line.find(k, 0, first_real_digit_idx + 1)
            if idx > -1: first_real_digit, first_real_digit_idx = v, idx

            ridx = line.rfind(k, last_real_digit_idx + 1, len(line))
            if ridx > -1: last_real_digit, last_real_digit_idx = v, ridx

    return int(f'{first_real_digit}{last_real_digit}')


if __name__ == "__main__":
    timer = utils.Timer()

    # Part 1
    # timer.start()
    # print(sum(get_calibration_value(line) for line in utils.read_str_lines()))
    # timer.stop()  #  43.44ms

    # Part 2
    timer.start()
    print(sum(get_calibration_value(line, as_letters=True) for line in utils.read_str_lines()))
    timer.stop()  # 36.53ms
