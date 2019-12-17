import numpy as np


def problem16a(n_phases, input_str=None, pattern=(0, 1, 0, -1)):
    if input_str is None:
        file_name = 'problem16.txt'
        with open(file_name) as file_obj:
            input_str = file_obj.read().strip()
    digits = np.array([int(char) for char in input_str])
    pattern = np.array(pattern)
    n_digits = len(digits)
    output = np.zeros(n_digits, dtype=np.int8)
    for _ in range(n_phases):
        for idigit in range(n_digits):
            rep_pattern = np.repeat(pattern, idigit + 1)
            n_tiles = np.ceil((n_digits + 1) / len(rep_pattern))
            n_tiles = int(n_tiles)
            tiled_pattern = np.tile(rep_pattern, n_tiles)
            prod_sum = np.sum(digits * tiled_pattern[1:n_digits+1])
            output[idigit] = np.abs(prod_sum) % 10
        digits = output
    output_str = ''.join([str(val) for val in output])
    return output_str


def test_problem16a():
    test_input = '12345678'
    assert '48226158' == problem16a(1, test_input)
    assert '34040438' == problem16a(2, test_input)
    assert '03415518' == problem16a(3, test_input)
    test_input = '80871224585914546619083218645595'
    assert '24176176' == problem16a(100, test_input)[:8]
    test_input = '19617804207202209144916044189917'
    assert '73745418' == problem16a(100, test_input)[:8]
    test_input = '69317163492948606335995924319873'
    assert '52432133' == problem16a(100, test_input)[:8]


if __name__ == '__main__':
    test_problem16a()
    print(problem16a(100)[:8])
