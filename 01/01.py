import utils

DIGITS = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

def get_calibration_value(line, as_letters=False):
    stripped = [c for c in line if c in [str(d) for d in range(1, 10)]]
    first_real_digit, last_real_digit = stripped[0], stripped[-1]

    if as_letters:
        first_real_digit_idx, last_real_digit_idx = line.find(first_real_digit), line.rfind(last_real_digit)

        for i, word in enumerate(DIGITS):
            if (idx := line.find(word, 0, first_real_digit_idx + 1)) > -1:
                first_real_digit, first_real_digit_idx = str(i + 1), idx

            if (ridx := line.rfind(word, last_real_digit_idx + 1)) > -1:
                last_real_digit, last_real_digit_idx = str(i + 1), ridx

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
