import numpy as np


def problem16a(input_str=None, n_phases=100, pattern=(0, 1, 0, -1)):
    if input_str is None:
        file_name = 'problem16.txt'
        with open(file_name) as file_obj:
            input_str = file_obj.read().strip()
    digits = np.array([int(char) for char in input_str])
    pattern = np.array(pattern)
    n_digits = len(digits)
    output = np.zeros(n_digits, dtype=np.int8)
    for _ in range(n_phases):
        cumsum = np.cumsum(digits)
        backwards_cumsum = np.cumsum(digits[:n_digits//2-1:-1])
        product_array = np.zeros((n_digits, n_digits), dtype=np.int8)
        for idigit in range(int(np.ceil(n_digits/2))):
            rep_pattern = np.repeat(pattern, idigit + 1)
            n_tiles = int(np.ceil((n_digits + 1) / len(rep_pattern)))
            tiled_pattern = np.tile(rep_pattern, n_tiles)
            product_array[idigit] = tiled_pattern[1:n_digits+1]
        prod_sum = np.sum(digits * product_array, axis=1)
        prod_sum[n_digits//2:] = backwards_cumsum[::-1]
        output = np.abs(prod_sum) % 10
        digits = output
    output_str = ''.join([str(val) for val in output[:8]])
    return output_str

def problem16b(input_str=None, n_phases=100, multiplier=10000):
    # this only works for the pattern (0, 1, 0, -1) and for cases where the
    # offset is >= half the length of the nubmer of digits
    if input_str is None:
        file_name = 'problem16.txt'
        with open(file_name) as file_obj:
            input_str = file_obj.read().strip()
    offset = int(input_str[:7])
    digits = np.tile(np.array([int(char) for char in input_str]), multiplier)
    assert offset >= len(digits)//2, "Offset must be >= half the number of digits."
    digits = digits[offset:]
    output = np.zeros(len(digits), dtype=np.int64)
    for iphase in range(n_phases):
        backwards_cumsum = np.cumsum(digits[::-1])
        output = backwards_cumsum[::-1]
        output = np.abs(output) % 10
        digits = output
    message = ''.join([str(val) for val in output[:8]])
    return message


def test_problem16a():
    test_input = '12345678'
    assert '48226158' == problem16a(test_input, 1)
    assert '34040438' == problem16a(test_input, 2)
    assert '03415518' == problem16a(test_input, 3)
    test_input = '80871224585914546619083218645595'
    assert '24176176' == problem16a(test_input)
    test_input = '19617804207202209144916044189917'
    assert '73745418' == problem16a(test_input)
    test_input = '69317163492948606335995924319873'
    assert '52432133' == problem16a(test_input)


def test_problem16b():
    test_input = '03036732577212944063491565474664'
    message = problem16b(test_input)
    assert '84462026' == message


if __name__ == '__main__':
    test_problem16a()
    print(problem16a())
    test_problem16b()
    print(problem16b())
