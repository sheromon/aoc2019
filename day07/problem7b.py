from itertools import permutations

import numpy as np

from intcode import Computer


def check_sequence(program):
    perms = permutations(range(5, 10))
    best_perm = None
    max_output = 0
    for sequence in perms:
        input_val = 0
        computers = {
            'A': Computer(np.copy(program), [input_val, sequence[0]]),
            'B': Computer(np.copy(program), [sequence[1]]),
            'C': Computer(np.copy(program), [sequence[2]]),
            'D': Computer(np.copy(program), [sequence[3]]),
            'E': Computer(np.copy(program), [sequence[4]]),
        }
        routing = {
            'A': 'B',
            'B': 'C',
            'C': 'D',
            'D': 'E',
            'E': 'A',
        }
        amp = 'A'
        last_output = None
        while not all([comp.done for comp in computers.values()]):
            output = computers[amp].run()
            next_amp = routing[amp]
            computers[next_amp].input_list.insert(0, output)
            amp = next_amp
            if output is not None:
                last_output = output

        if last_output > max_output:
            best_perm = sequence
            max_output = last_output
    return max_output, best_perm


def problem7b():
    file_name = 'day07/problem7.txt'
    int_array = np.loadtxt(file_name, np.int32, delimiter=',')
    return check_sequence(int_array)[0]


def test_problem7b():
    test_program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
                    27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    results = check_sequence(test_program)
    print(results)
    test_program = [
        3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
        -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
        53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
    results = check_sequence(test_program)
    print(results)


if __name__ == '__main__':
    test_problem7b()
    print(problem7b())
