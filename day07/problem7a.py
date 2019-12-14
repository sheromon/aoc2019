from itertools import permutations

import numpy as np

from intcode import Computer


def check_sequence(program):
    perms = permutations(range(5))
    best_perm = None
    max_output = 0
    for sequence in perms:
        input_val = 0
        for phase in sequence:
            computer = Computer(np.copy(program), [input_val, phase])
            output = computer.run()
            input_val = output
        if output > max_output:
            best_perm = sequence
            max_output = output
    return max_output, best_perm


def problem7a():
    file_name = 'day07/problem7.txt'
    int_array = np.loadtxt(file_name, np.int32, delimiter=',')
    return check_sequence(int_array)[0]


def test_problem7a():
    test_program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    results = check_sequence(test_program)
    assert results == (43210, (4, 3, 2, 1, 0))


if __name__ == '__main__':
    test_problem7a()
    print(problem7a())
