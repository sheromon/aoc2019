from itertools import permutations

import numpy as np


def parse_instruction(instruction):
    modes = []
    num_params = 0
    opcode = instruction % 100
    if opcode in [1, 2, 7, 8]:
        num_params = 3
    elif opcode in [3, 4]:
        num_params = 1
    elif opcode in [5, 6]:
        num_params = 2
    modes = (instruction // 10**np.arange(2, 2+num_params)) % 10
    return opcode, modes, num_params


def run_program(int_array, input_vals):
    pointer = 0
    output_val = None
    while True:
        opcode, modes, num_params = parse_instruction(int_array[pointer])
        if opcode == 99:
            return output_val

        params = int_array[pointer+1:pointer+1+num_params]
        if opcode in [1, 2, 3, 7, 8]:
            modes, last_mode = modes[:-1], modes[-1]
            assert last_mode == 0  # should always be in position mode
            params, pos = params[:-1], params[-1]
        params = [val if mode else int_array[val]
                  for (val, mode) in zip(params, modes)]

        if opcode in [1, 2, 7, 8]:
            if opcode == 1:
                val = np.sum(params)
            elif opcode == 2:
                val = np.prod(params)
            elif opcode == 7:  # less than
                val = int(params[0] < params[1])
            elif opcode == 8:  # equals
                val = int(params[0] == params[1])
            int_array[pos] = val
        elif opcode == 3:  # input
            int_array[pos] = input_vals.pop()
        elif opcode == 4:  # output
            output_val = params[0]
        elif opcode in [5, 6]:
            if opcode == 5:  # jump if true
                condition = params[0]
            elif opcode == 6:  # jump if false
                condition = not params[0]
            if condition:
                pointer = params[1]
                continue
        else:
            raise RuntimeError("Bad opcode {:d} at position {:d}".format(
                opcode, pointer))
        pointer += (1 + num_params)
    return None


def check_sequence(program):
    perms = permutations(range(5))
    best_perm = None
    max_output = 0
    for sequence in perms:
        input_val = 0
        for phase in sequence:
            output = run_program(np.copy(program), [input_val, phase])
            input_val = output
        if output > max_output:
            best_perm = sequence
            max_output = output
    return max_output, best_perm


def problem7a():
    file_name = 'problem7.txt'
    int_array = np.loadtxt(file_name, np.int32, delimiter=',')
    return check_sequence(int_array)[0]


def test_problem7a():
    test_program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    results = check_sequence(test_program)
    assert results == (43210, (4, 3, 2, 1, 0))


if __name__ == '__main__':
    test_problem7a()
    print(problem7a())
