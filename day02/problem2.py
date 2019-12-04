import copy

import numpy as np


def run_program(int_list):
    current_pos = 0
    while True:
        opcode = int_list[current_pos]
        if opcode == 99:
            break
        else:
            in_pos1 = int_list[current_pos + 1]
            in_pos2 = int_list[current_pos + 2]
            out_pos = int_list[current_pos + 3]
            if out_pos >= len(int_list):
                delta = len(int_list) - out_pos
                int_list += (delta + 1) * [None]
            if opcode == 1:
                int_list[out_pos] = int_list[in_pos1] + int_list[in_pos2]
            elif opcode == 2:
                int_list[out_pos] = int_list[in_pos1] * int_list[in_pos2]
            else:
                raise RuntimeError("Bad opcode {:d} at position {:d}".format(
                    opcode, current_pos))
        current_pos += 4
    return int_list

def test_computer():
    test_int_list = [1,0,0,0,99]
    result = run_program(test_int_list)
    assert [2,0,0,0,99] == result, "Incorrect result for {}".format(test_int_list)
    test_int_list = [2,3,0,3,99]
    result = run_program(test_int_list)
    assert [2,3,0,6,99] == result, "Incorrect result for {}".format(test_int_list)
    test_int_list = [2,4,4,5,99]
    result = run_program(test_int_list)
    assert [2,4,4,5,99,9801] == result, "Incorrect result for {}".format(test_int_list)
    test_int_list = [1,1,1,4,99,5,6,0,99]
    result = run_program(test_int_list)
    assert [30,1,1,4,2,5,6,0,99] == result, "Incorrect result for {}".format(test_int_list)
    test_int_list = [1,9,10,3,2,3,11,0,99,30,40,50]
    result = run_program(test_int_list)
    assert [3500,9,10,70,2,3,11,0,99,30,40,50] == result, "Incorrect result for {}".format(test_int_list)

def read_input():
    file_name = 'problem2.txt'
    return np.loadtxt(file_name, np.int32, delimiter=',').tolist()

def problem2a():
    int_list = read_input()
    int_list[1] = 12
    int_list[2] = 2            
    return run_program(int_list)[0]

def problem2b():
    int_list = read_input()
    done = False
    for noun in range(100):
        for verb in range(100):
            new_int_list = copy.deepcopy(int_list)
            new_int_list[1] = noun
            new_int_list[2] = verb
            output = run_program(new_int_list)[0]
            if output == 19690720:
                return 100 * noun + verb
    return None


if __name__ == '__main__':
    test_computer()
    print(problem2a())
    print(problem2b())
