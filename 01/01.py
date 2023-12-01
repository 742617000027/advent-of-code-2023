import utils


def get_calibration_value(line, as_letters=False):
    stripped = [c for c in line if c in [str(d) for d in range(10)]]
    if not as_letters:
        return int(f'{stripped[0]}{stripped[-1]}')

    d = {
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

    first_real_digit = stripped[0]
    first_real_digit_idx = line.find(first_real_digit)

    last_real_digit = stripped[-1]
    last_real_digit_idx = len(line) - line[::-1].find(last_real_digit) - 1

    for k, v in d.items():
        idx = find_all(k, line)
        if len(idx) > 0 and idx[0] < first_real_digit_idx:
            first_real_digit = v
            first_real_digit_idx = idx[0]
        if len(idx) > 0 and idx[-1] > last_real_digit_idx:
            last_real_digit = v
            last_real_digit_idx = idx[-1]

    return int(f'{first_real_digit}{last_real_digit}')


def find_all(needle, haystack):
    ret = []
    idx = 0
    while True:
        idx = haystack.find(needle, idx)
        if idx == -1:
            break
        ret.append(idx)
        idx += len(needle)
    return ret


if __name__ == "__main__":
    timer = utils.Timer()

    # Part 1
    # timer.start()
    # print(sum(get_calibration_value(line) for line in utils.read_str_lines()))
    # timer.stop()  #  43.44ms

    # Part 2
    timer.start()
    print(sum(get_calibration_value(line, as_letters=True) for line in utils.read_str_lines()))
    timer.stop()  # 37.56ms

